# 语法检查器 for ERA BASIC 脚本文件 (.ERB)
# 用法：在终端中输入 python erb_check.py ./文件夹名 （可选：--fix，强制缩进）

import sys
import re

class ErbLinter:
    def __init__(self, indent_char='\t'):
        # --- 1. 初始化基础变量 ---
        self.indent_char = indent_char
        self.indent_level = 0
        self.formatted_lines = []
        self.errors = []      # 语法错误
        self.warnings = []    # 逻辑警告
        self.stack = []       # 用于跟踪代码块结构

        # --- 2. 定义基础规则 ---
        # 1=开始(缩进+1), 2=结束(缩进-1), 3=中间(缩进-1后恢复), 4=单行(下行缩进+1)
        self.rules = {
            # 流程控制 - 开始
            'IF': 1, 'SELECTCASE': 1, 'FOR': 1, 'WHILE': 1, 'DO': 1, 'REPEAT': 1,
            'DATALIST': 1, 'TRYCALLLIST': 1, 'NOSKIP': 1,
            # (PRINTDATA 系列稍后动态生成)

            # 流程控制 - 结束
            'ENDIF': 2, 'ENDSELECT': 2, 'NEXT': 2, 'WEND': 2, 'LOOP': 2, 'REND': 2,
            'ENDLIST': 2, 'ENDCATCH': 2, 'ENDNOSKIP': 2,
            # (ENDDATA 稍后动态生成)

            # 流程控制 - 中间跳转
            'ELSE': 3, 'ELSEIF': 3, 'CASE': 3, 'CASEELSE': 3, 'DATAFORM': 3,
            
            # 单行控制
            'SIF': 4, 
        }

        # --- 3. 定义配对规则 (结束标签: [允许的开始标签列表]) ---
        self.pairs = {
            'ENDIF': ['IF'], 
            'ENDSELECT': ['SELECTCASE'], 
            'NEXT': ['FOR'],
            'WEND': ['WHILE'], 
            'LOOP': ['DO'], 
            'REND': ['REPEAT'],
            'ENDLIST': ['DATALIST', 'TRYCALLLIST'],
            # (ENDDATA 稍后动态生成)
        }

        # --- 4. 动态生成 PRINTDATA 及其变体规则 ---
        # 变体包括：PRINTDATA, PRINTDATAL, PRINTDATAW
        #           PRINTDATAK, PRINTDATAKL, PRINTDATAKW
        #           PRINTDATAD, PRINTDATADL, PRINTDATADW
        
        pd_bases = ['PRINTDATA', 'PRINTDATAK', 'PRINTDATAD']
        pd_suffixes = ['', 'L', 'W']

        # 初始化 ENDDATA 规则
        self.rules['ENDDATA'] = 2
        self.pairs['ENDDATA'] = [] 

        for base in pd_bases:
            for suffix in pd_suffixes:
                variant = base + suffix  # 比如 PRINTDATAKW
                
                # 注册为“块开始”
                self.rules[variant] = 1 
                
                # 注册配对归属 (它们都由 ENDDATA 关闭)
                self.pairs['ENDDATA'].append(variant)

    def parse_line(self, line):
        line = line.strip()
        if not line: return None, "", "", ""
        
        comment = ""
        code = line
        if ';' in line:
            parts = line.split(';', 1)
            code = parts[0].strip()
            comment = ';' + parts[1]
        elif line.startswith('//'):
            code = ""
            comment = line
            
        if not code: return None, "", "", comment

        # 分离 Keyword 和 Arguments
        # 例如: "IF A == 1" -> Keyword="IF", Args="A == 1"
        match = re.match(r'^([A-Za-z0-9_]+)(?:\s+(.*))?$', code)
        if match:
            keyword = match.group(1).upper()
            args = match.group(2) if match.group(2) else ""
            return keyword, args, code, comment
        return None, "", "", comment

    def check_syntax_and_logic(self, keyword, args, line_num):
        """核心逻辑检查函数"""
        
        # --- 1. 基础语法规则检查 ---
        
        # 规则：ELSE / CASEELSE 后不能跟条件
        if keyword in ['ELSE', 'CASEELSE'] and args:
            self.errors.append(f"Line {line_num}: Syntax Error - '{keyword}' should not have conditions. Found: '{args}'")

        # 规则：ELSEIF / CASE 后必须跟条件
        if keyword in ['ELSEIF', 'CASE'] and not args:
             self.errors.append(f"Line {line_num}: Syntax Error - '{keyword}' requires a condition/value.")

        # --- 2. 流程控制逻辑检查 (基于栈) ---
        
        if self.stack:
            parent = self.stack[-1] # 获取当前所在的代码块信息
            parent_kw = parent['keyword']

            # 规则：ELSE 后不能再有 ELSEIF/ELSE
            if keyword in ['ELSE', 'ELSEIF', 'CASE', 'CASEELSE']:
                if parent.get('has_else', False):
                    self.errors.append(f"Line {line_num}: Syntax Error - Unreachable '{keyword}' found after an 'ELSE/CASEELSE' in the same block.")

            # 标记当前块已经出现了 ELSE
            if keyword in ['ELSE', 'CASEELSE']:
                parent['has_else'] = True

            # 规则：CASE 必须在 SELECTCASE 里
            if keyword in ['CASE', 'CASEELSE'] and parent_kw != 'SELECTCASE':
                self.errors.append(f"Line {line_num}: Syntax Error - '{keyword}' found outside of SELECTCASE (Current block: {parent_kw}).")

            # 规则：ELSEIF 必须在 IF 里
            if keyword in ['ELSE', 'ELSEIF'] and parent_kw != 'IF':
                self.errors.append(f"Line {line_num}: Syntax Error - '{keyword}' found outside of IF (Current block: {parent_kw}).")

            # --- 3. RAND 逻辑深度检查 ---
            
            # 场景 A: 检查 SELECTCASE RAND:X 里的 CASE 越界
            # 这里的逻辑是：如果 SELECTCASE 是 RAND:4，那么 CASE 4 是永远进不去的
            if keyword == 'CASE' and parent_kw == 'SELECTCASE' and parent.get('rand_max'):
                rand_max = parent['rand_max']
                # 解析 CASE 的参数，支持 "CASE 1", "CASE 1, 2", "CASE 1 TO 3"
                case_args = args.replace(',', ' ').split()
                for arg in case_args:
                    # 简单检查数字
                    if arg.isdigit():
                        val = int(arg)
                        if val >= rand_max:
                            self.warnings.append(f"Line {line_num}: Logic Warning - 'CASE {val}' is unreachable. 'SELECTCASE RAND:{rand_max}' only returns 0 to {rand_max-1}.")
                    # 简单检查 TO 范围 (例如 3 TO 5)
                    # 这里简化处理，如果这一行包含 TO，做一个正则提取
                    range_match = re.search(r'(\d+)\s*TO\s*(\d+)', args, re.IGNORECASE)
                    if range_match:
                        start, end = int(range_match.group(1)), int(range_match.group(2))
                        if start >= rand_max:
                            self.warnings.append(f"Line {line_num}: Logic Warning - Range '{start} TO {end}' is entirely unreachable given RAND:{rand_max}.")

        # --- 4. 单行逻辑检查 ---
        
        # 场景 B: IF/ELSEIF RAND:1
        # RAND:1 永远返回 0。在 IF 中 0 为 False。所以 IF RAND:1 永远不执行。
        # 检查 args 里是否有 RAND:1
        if keyword in ['IF', 'ELSEIF', 'SIF']:
            # 使用正则匹配独立的单词 RAND:1，防止匹配到 RAND:10
            if re.search(r'\bRAND:1\b', args, re.IGNORECASE):
                self.warnings.append(f"Line {line_num}: Logic Warning - 'RAND:1' always returns 0 (False). This branch will never execute.")

    def analyze_select_case_start(self, args):
        """分析 SELECTCASE 的条件，看是否是 RAND"""
        # 匹配 SELECTCASE RAND:X
        match = re.search(r'RAND:(\d+)', args, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return None

    def process_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f: lines = f.readlines()
        except:
            with open(file_path, 'r', encoding='shift-jis') as f: lines = f.readlines()

        next_indent_bonus = 0

        for i, raw_line in enumerate(lines):
            line_num = i + 1
            keyword, args, code, comment = self.parse_line(raw_line)

            if keyword is None:
                # 保持缩进打印注释/空行
                curr = max(0, self.indent_level + next_indent_bonus)
                self.formatted_lines.append((self.indent_char * curr) + comment)
                if code == "": continue

            rtype = self.rules.get(keyword, 0)
            
            # --- 运行逻辑检查 ---
            self.check_syntax_and_logic(keyword, args, line_num)

            # --- 缩进计算 (同上一版，略微调整) ---
            offset = 0
            if rtype == 2: # End
                self.indent_level -= 1
                # 栈检查
                if not self.stack:
                    self.errors.append(f"Line {line_num}: Unexpected '{keyword}'. No block is open.")
                else:
                    opener = self.stack.pop()
                    if keyword in self.pairs and opener['keyword'] not in self.pairs[keyword]:
                        self.errors.append(f"Line {line_num}: Mismatch! '{keyword}' closes '{opener['keyword']}' (Line {opener['line']}).")
            
            elif rtype == 3: # Middle (ELSE, CASE)
                offset = -1

            if self.indent_level < 0: self.indent_level = 0
            
            print_level = max(0, self.indent_level + offset + next_indent_bonus)
            
            # 格式化输出
            full_code = f"{keyword} {args}".strip()
            out_line = f"{self.indent_char * print_level}{full_code}"
            if comment: out_line += f" {comment}"
            self.formatted_lines.append(out_line)

            # 重置 SIF 奖励
            is_sif = (rtype == 4)
            next_indent_bonus = 1 if is_sif else 0

            # 压栈
            if rtype == 1: # Start Block
                self.indent_level += 1
                # 创建上下文对象
                ctx = {
                    'keyword': keyword,
                    'line': line_num,
                    'has_else': False,
                    'rand_max': None
                }
                # 特殊处理：如果是 SELECTCASE，分析是否是 RAND 模式
                if keyword == 'SELECTCASE':
                    ctx['rand_max'] = self.analyze_select_case_start(args)
                
                self.stack.append(ctx)

            if keyword and keyword.startswith('@'):
                self.indent_level = 0
                self.stack = []
                next_indent_bonus = 0

    def report(self):
        print("\n" + "="*40)
        print(" ERA BASIC LINTER REPORT ")
        print("="*40)
        
        has_issue = False
        if self.errors:
            has_issue = True
            for e in self.errors:
                print(f"\033[91m[ERROR] {e}\033[0m") # Red
        
        if self.warnings:
            has_issue = True
            for w in self.warnings:
                print(f"\033[93m[WARN ] {w}\033[0m") # Yellow (Orange)

        if not has_issue:
            print("\033[92mAll checks passed. Syntax looks good!\033[0m")
        
        # 检查未闭合的块
        if self.stack:
            print("-" * 20)
            for item in self.stack:
                print(f"\033[91m[FATAL] Unclosed block '{item['keyword']}' from Line {item['line']}\033[0m")

    def save_file(self, file_path):
        """将整理好的代码写回文件"""
        # 为了安全，只有当文件内容真的改变了，或者确实需要修复时才写入
        # 这里我们直接写入
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                # 确保每行后面都有换行符
                f.write('\n'.join(self.formatted_lines))
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python erb_linter.py <script.erb>")
        # 这里的测试代码仅在没有文件输入时运行
        print("\n--- Running Internal Test ---")
        dummy_code = """
        @TEST_LOGIC
        IF RAND:1
            PRINT This is dead code
        ENDIF

        SELECTCASE RAND:3
            CASE 0
                PRINT Zero
            CASE 1, 2
                PRINT OK
            CASE 3
                PRINT Unreachable!
            CASE 4 TO 10
                PRINT Way out of bounds
        ENDSELECT

        IF A == 1
            PRINT A
        ELSE
            PRINT B
            ELSEIF C == 1
                PRINT Syntax Error: ElseIf after Else
        ENDIF
        
        IF X == 1
        ELSE A == 1
            PRINT Syntax Error: Else has condition
        ENDIF
        """
import os

def process_target(target_path, is_batch=False, apply_fix=False):
    linter = ErbLinter()
    linter.process_file(target_path)
    
    has_error = len(linter.errors) > 0
    
    # 打印错误报告
    if has_error or linter.warnings:
        # 如果是批量模式，只在出错时打印文件名
        if is_batch:
            print(f"\n📂 Checking: {target_path}")
        linter.report()
    elif not is_batch:
        # 单文件且无错，也打印报告
        linter.report()

    # --- 核心修改：保存文件 ---
    if apply_fix:
        # 即使有错误，也尝试保存缩进，因为缩进突变能帮你找到错误位置
        # 但为了防止严重语法错误导致文件损毁，通常建议备份
        # 这里直接覆盖，请确保你使用了 Git 或有备份
        linter.save_file(target_path)
        if not is_batch: 
            print(f"💾 File updated: {target_path}")
            
    return not has_error

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Check only: python erb_check.py <path>")
        print("  Check & Fix: python erb_check.py <path> --fix")
        sys.exit(1)

    input_path = sys.argv[1]
    
    # 检查是否开启修复模式
    apply_fix = '--fix' in sys.argv

    if apply_fix:
        print("\n⚠️  WARNING: FIX MODE ENABLED ⚠️")
        print("Files will be overwritten with formatted indentation.")
        print("Ensure you have a backup or use Git before proceeding.")
        print("Starting in 3 seconds...")
        import time
        time.sleep(3)

    if os.path.isfile(input_path):
        process_target(input_path, is_batch=False, apply_fix=apply_fix)

    elif os.path.isdir(input_path):
        print(f"🚀 Starting batch check in: {input_path}")
        if apply_fix: print("🔧 Auto-fix: ON")
        print("="*40)
        
        error_count = 0
        file_count = 0
        
        for root, dirs, files in os.walk(input_path):
            for file in files:
                if file.lower().endswith('.erb'):
                    file_path = os.path.join(root, file)
                    file_count += 1
                    # 进度条
                    if file_count % 10 == 0:
                        print(".", end="", flush=True)
                    
                    if not process_target(file_path, is_batch=True, apply_fix=apply_fix):
                        error_count += 1
        
        print(f"\n\n{'='*40}")
        print(f"✅ Batch processing complete.")
        print(f"📄 Files scanned: {file_count}")
        if apply_fix:
            print(f"💾 All scanned files have been re-indented.")
