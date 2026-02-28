import os
import csv
import glob
import re

# ================= 配置区域 =================
# CSV文件夹路径
CSV_DIR = './CSV'
# 生成的ERH头文件存放路径
OUTPUT_DIR = './ERB/Headers'
# 需要排除的文件名（支持通配符 *）
EXCLUDE_FILES = [
    'Train.csv',       # 指令定义，非枚举
    'Chara*.csv',      # 角色模板，非枚举
    'GameBase.csv',    # 系统配置
    '_*.csv',          # 惯例：下划线开头通常是临时文件
    'Str.csv',         # 这里的索引通常不是固定的
    'VarSize.csv'      # 变量大小定义
]

# 字符编码 (Emuera通常是 UTF-8 或 Shift-JIS)
# 这里使用 utf-8-sig 以兼容带BOM的文件，如果乱码请尝试 'cp932' (即Shift-JIS)
FILE_ENCODING = 'utf-8-sig' 
# ===========================================

def sanitize_var_name(name):
    """
    清洗变量名，使其符合ERB常量命名规范
    1. 去除空格、制表符
    2. 去除括号和其他特殊符号
    3. 如果是数字开头，添加下划线前缀
    """
    if not name:
        return ""
    
    # 去除首尾空白
    name = name.strip()
    
    # 替换常见的分隔符为下划线
    name = re.sub(r'[ \t　\-]', '_', name)
    
    # 去除不仅限于ERB变量名的字符 (保留中日韩字符、字母、数字、下划线)
    # 过滤掉 [ ] 【 】 ( ) 「 」 . + * / ? ! 等
    name = re.sub(r'[\[\]【】「」\(\)\.\+\*\/,?!:;<>@#$%^&|~`\'"“”]', '', name)
    
    # 如果处理后为空，直接返回
    if not name:
        return ""

    # 如果首字符是数字，加下划线前缀 (ERB变量不能以数字开头)
    if name[0].isdigit():
        name = '_' + name
        
    return name

def should_skip(filename):
    """检查文件是否在排除列表中"""
    from fnmatch import fnmatch
    for pattern in EXCLUDE_FILES:
        if fnmatch(filename, pattern):
            return True
    return False

def parse_file(filepath, mapping, source_name):
    """
    解析单个CSV/ALS文件并更新映射表
    mapping: dict { 'SanitizedName': ID }
    """
    if not os.path.exists(filepath):
        return

    print(f"正在读取: {filepath}")
    try:
        with open(filepath, mode='r', encoding=FILE_ENCODING, errors='replace') as f:
            # 使用csv reader处理引号和逗号
            reader = csv.reader(f)
            
            for row in reader:
                # 跳过空行或太短的行
                if not row or len(row) < 2:
                    continue
                
                raw_id = row[0].strip()
                raw_name = row[1].strip()
                
                # 跳过注释行 (;开头)
                if raw_id.startswith(';'):
                    continue
                
                # 尝试解析ID
                try:
                    # 处理可能的注释 (如 "100 ;注释")
                    id_val = int(raw_id.split(';')[0].strip())
                except ValueError:
                    continue # ID不是数字，跳过
                
                # 处理名字中的行内注释 (截取 ; 之前的部分)
                if ';' in raw_name:
                    raw_name = raw_name.split(';')[0].strip()
                
                if not raw_name:
                    continue

                # 清洗变量名
                clean_name = sanitize_var_name(raw_name)
                if not clean_name:
                    continue
                
                # 冲突检测
                if clean_name in mapping:
                    if mapping[clean_name] != id_val:
                        print(f"  [警告] 名称冲突: '{clean_name}' 在 {source_name} 中被定义为 {id_val}, 但此前已被定义为 {mapping[clean_name]}。保留旧值。")
                else:
                    mapping[clean_name] = id_val

    except Exception as e:
        print(f"  [错误] 读取文件失败 {filepath}: {e}")

def main():
    # 确保输出目录存在
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"创建目录: {OUTPUT_DIR}")

    # 获取所有CSV文件
    csv_files = glob.glob(os.path.join(CSV_DIR, '*.csv'))
    
    for csv_path in csv_files:
        filename = os.path.basename(csv_path)
        
        # 检查黑名单
        if should_skip(filename):
            print(f"跳过排除文件: {filename}")
            continue
            
        # 提取基础名称 (例如 Item.csv -> Item)
        base_name = os.path.splitext(filename)[0]
        prefix = base_name.upper() # 前缀大写，如 ITEM
        
        # 数据存储 { Name: ID }
        const_map = {}
        
        # 1. 读取主CSV文件
        parse_file(csv_path, const_map, filename)
        
        # 2. 读取对应的 ALS 文件
        # 逻辑：寻找同目录下同名的 .als 文件
        # 兼容 "Item.als" 和 "Item - 副本.als.txt" 这种情况有点复杂，
        # 这里优先匹配标准的 base_name.als
        als_path = os.path.join(CSV_DIR, base_name + '.als')
        if os.path.exists(als_path):
             parse_file(als_path, const_map, base_name + '.als')
        
        # 尝试匹配其他可能的ALS命名 (如 Item - Copy.als 等，如果需要的话)
        # 这里简单起见，只匹配标准ALS。如果你有很多非标准命名的ALS，需要手动改名或增加逻辑。
        
        # 3. 生成ERH内容
        if not const_map:
            continue
            
        erh_filename = f"AutoConst_{base_name}.ERH"
        erh_path = os.path.join(OUTPUT_DIR, erh_filename)
        
        try:
            with open(erh_path, 'w', encoding=FILE_ENCODING) as f:
                f.write(f"; =====================================================\n")
                f.write(f"; 自动生成的常量头文件 - 源文件: {filename}\n")
                f.write(f"; 请勿手动修改此文件，请修改CSV/ALS后重新运行生成脚本\n")
                f.write(f"; =====================================================\n\n")
                
                # 按ID排序，方便阅读
                sorted_items = sorted(const_map.items(), key=lambda x: x[1])
                
                for name, id_val in sorted_items:
                    # 生成格式: #DIM CONST PREFIX_NAME = ID
                    # 例如: #DIM CONST ITEM_好吃的鱼 = 708
                    line = f"#DIM CONST {prefix}_{name} = {id_val}\n"
                    f.write(line)
            
            print(f"生成成功: {erh_path} (包含 {len(const_map)} 个常量)")
            
        except Exception as e:
            print(f"写入文件失败 {erh_path}: {e}")

    print("\n所有操作完成。")
    input("按回车键退出...")

if __name__ == '__main__':
    main()