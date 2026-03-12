import os
import subprocess
import fnmatch
from datetime import datetime

class GitUpdater:
    def __init__(self):
        self.repo_path = os.path.dirname(os.path.abspath(__file__))
        self.nightly_branch = "nightly-build"
        self.developing_branch = "developing"
        self.update_folder = os.path.join(self.repo_path, "更新文件")
        self.backup_folder = os.path.join(self.repo_path, "备份_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
        self.remote_prefix = "main"
        self.gitignore_patterns = self.load_gitignore()
        
    def load_gitignore(self):
        """加载并解析.gitignore文件"""
        gitignore_path = os.path.join(self.repo_path, ".gitignore")
        patterns = []
        
        if os.path.exists(gitignore_path):
            print("\n加载.gitignore文件...")
            try:
                with open(gitignore_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        line = line.strip()
                        # 跳过空行和注释
                        if not line or line.startswith('#') or line.startswith(';'):
                            continue
                        # 移除转义的反斜杠
                        line = line.replace('\\', '')
                        patterns.append(line)
                print(f"  ✓ 加载了 {len(patterns)} 个忽略模式")
            except Exception as e:
                print(f"  ❌ 加载.gitignore失败: {str(e)}")
        
        return patterns
    
    def is_ignored(self, filepath):
        """检查文件是否被.gitignore忽略"""
        for pattern in self.gitignore_patterns:
            # 处理目录模式（以/开头的目录）
            if pattern.startswith('/') and not pattern.endswith('/'):
                pattern_dir = pattern[1:]
                if filepath == pattern_dir or filepath.startswith(pattern_dir + '/'):
                    return True
            # 处理目录模式（以/结尾的目录）
            elif pattern.endswith('/'):
                pattern_dir = pattern.rstrip('/')
                if filepath == pattern_dir or filepath.startswith(pattern_dir + '/'):
                    return True
            # 处理普通目录模式
            elif '/' in pattern and not pattern.endswith('*'):
                # 检查是否是目录匹配
                if filepath == pattern or filepath.startswith(pattern + '/'):
                    return True
            # 处理文件模式
            elif fnmatch.fnmatch(filepath, pattern):
                return True
            elif fnmatch.fnmatch(os.path.basename(filepath), pattern):
                return True
        return False
    
    def detect_remote_branches(self):
        print("\n检测远程分支...")
        
        output, returncode = self.run_git_command(["git", "branch", "-r"])
        
        if returncode != 0 or not output:
            print("❌ 无法获取远程分支列表")
            return False
        
        branches = [line.strip() for line in output.split('\n') if line.strip()]
        
        print(f"  找到 {len(branches)} 个远程分支:")
        
        for branch in branches:
            print(f"    - {branch}")
        
        if not branches:
            return False
        
        first_branch = branches[0]
        if '/' in first_branch:
            self.remote_prefix = first_branch.split('/')[0]
            print(f"\n  使用远程前缀: {self.remote_prefix}")
        
        return True
        
    def run_git_command(self, command):
        try:
            result = subprocess.run(
                command,
                cwd=self.repo_path,
                capture_output=True,
                timeout=30
            )
            
            if result.stdout:
                output = result.stdout.decode('utf-8', errors='ignore').strip()
            else:
                output = ""
            
            return output, result.returncode
        except subprocess.TimeoutExpired:
            print(f"  ❌ Git命令超时: {' '.join(command)}")
            return "", -1
        except Exception as e:
            print(f"  ❌ Git命令错误: {str(e)}")
            return "", -1
    
    def check_git_repository(self):
        print("\n检查Git仓库...")
        
        output, returncode = self.run_git_command(["git", "rev-parse", "--git-dir"])
        
        if returncode == 0:
            print("✓ 当前目录是Git仓库")
            return True
        else:
            print("❌ 当前目录不是Git仓库")
            return False
    
    def check_remote(self):
        print("\n检查远程仓库...")
        
        output, returncode = self.run_git_command(["git", "remote", "-v"])
        
        if returncode == 0 and output:
            print(f"✓ 远程仓库: {output.split()[1]}")
            return True
        else:
            print("❌ 未找到远程仓库")
            return False
    
    def fetch_branches(self):
        print("\n获取最新分支信息...")
        
        output, returncode = self.run_git_command(["git", "fetch", "--all"])
        
        if returncode == 0:
            print("✓ 分支信息已更新")
            return True
        else:
            print("❌ 获取分支信息失败")
            return False
    
    def get_branch_info(self, branch):
        output, returncode = self.run_git_command(["git", "show", "-s", "--format=%H", f"{self.remote_prefix}/{branch}"])
        
        if returncode == 0 and output:
            sha = output[:7]
            
            output2, returncode2 = self.run_git_command(["git", "show", "-s", "--format=%ci", f"{self.remote_prefix}/{branch}"])
            if returncode2 == 0 and output2:
                date = output2[:19].replace('T', ' ')
            else:
                date = "Unknown"
            
            output3, returncode3 = self.run_git_command(["git", "show", "-s", "--format=%s", f"{self.remote_prefix}/{branch}"])
            if returncode3 == 0 and output3:
                message = output3
            else:
                message = "Unknown"
            
            return {
                'sha': sha,
                'date': date,
                'message': message
            }
        return None
    
    def get_changed_files(self, branch1, branch2):
        print("\n获取文件变更列表...")
        
        result = subprocess.run(
            ["git", "diff", "--name-status", "-z",
             f"{self.remote_prefix}/{branch2}", f"{self.remote_prefix}/{branch1}"],
            cwd=self.repo_path,
            capture_output=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print("❌ 获取文件变更失败")
            return []
        
        if not result.stdout:
            print("  没有文件变更")
            return []
        
        output = result.stdout.decode('utf-8', errors='ignore')
        entries = output.split('\x00')
        
        files_list = []
        i = 0
        while i < len(entries):
            entry = entries[i]
            
            if not entry:
                i += 1
                continue
            
            status = entry[0]
            filename = None
            
            if status in ['A', 'M', 'D']:
                if i + 1 < len(entries):
                    filename = entries[i + 1]
                    i += 2
                else:
                    i += 1
                    continue
            elif status.startswith('R') or status.startswith('C'):
                # 重命名或复制：R100 old_path new_path
                # 需要取两个路径：old_path（用于记录删除），new_path（用于复制）
                if i + 2 < len(entries):
                    old_filename = entries[i + 1]
                    new_filename = entries[i + 2]
                    i += 3
                    
                    # 对于重命名，旧文件视为删除
                    if status.startswith('R'):
                        if not self.is_ignored(old_filename):
                            files_list.append({
                                'filename': old_filename,
                                'status': 'removed'
                            })
                    
                    # 新文件视为新增/修改（这里标记为renamed以便区分）
                    if not self.is_ignored(new_filename):
                        files_list.append({
                            'filename': new_filename,
                            'status': 'renamed'
                        })
                    continue
                else:
                    i += 1
                    continue
            else:
                i += 1
                continue
            
            if not filename:
                continue
            
            status_map = {
                'A': 'added',
                'M': 'modified',
                'D': 'removed',
                'R': 'renamed',
                'C': 'copied'
            }
            
            # 检查文件是否被gitignore忽略
            if not self.is_ignored(filename):
                files_list.append({
                    'filename': filename,
                    'status': status_map.get(status, 'modified')
                })
            else:
                print(f"  ⚠️  跳过被.gitignore忽略的文件: {filename}")
        
        print(f"  ✓ 共找到 {len(files_list)} 个变更文件")
        return files_list
    
    def copy_file_from_git(self, file_path, branch):
        try:
            # 使用列表形式的命令，避免shell注入，且无需转义
            cmd = ["git", "cat-file", "-p", f"{self.remote_prefix}/{branch}:{file_path}"]
            
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return result.stdout
            else:
                # 尝试使用 show 命令作为备选，同样使用列表形式
                cmd2 = ["git", "show", f"{self.remote_prefix}/{branch}:{file_path}"]
                result2 = subprocess.run(
                    cmd2,
                    cwd=self.repo_path,
                    capture_output=True,
                    timeout=30
                )
                if result2.returncode == 0:
                    return result2.stdout
            
            print(f"  ❌ Git读取失败 ({file_path}): {result.stderr.decode('utf-8', errors='ignore').strip()}")
            return None
        except Exception as e:
            print(f"  ❌ Git命令异常: {str(e)}")
            return None
    
    def copy_files_to_update_folder(self, files_to_copy, branch):
        print(f"\n准备复制文件到更新文件夹...")
        
        # 创建详细日志文件
        log_path = os.path.join(self.repo_path, "update_debug_log.txt")
        self.log_file = open(log_path, 'w', encoding='utf-8')
        self.log(f"开始更新流程: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log(f"目标分支: {branch}")
        
        if os.path.exists(self.update_folder):
            import shutil
            shutil.rmtree(self.update_folder)
        os.makedirs(self.update_folder)
        
        total_files = len(files_to_copy)
        success_count = 0
        fail_count = 0
        removed_files = []
        
        to_copy = [f for f in files_to_copy if f['status'] != 'removed']
        to_clear = [f['filename'] for f in files_to_copy if f['status'] == 'removed']
        
        print(f"共需复制 {total_files} 个文件\n")
        self.log(f"总计文件: {total_files}, 需复制: {len(to_copy)}, 需清理: {len(to_clear)}")
        
        for i, file_info in enumerate(to_copy, 1):
            file_path = file_info['filename']
            status = file_info['status']
            
            content = self.copy_file_from_git(file_path, branch)
            if content is not None:
                local_file_path = os.path.join(self.update_folder, file_path)
                local_dir = os.path.dirname(local_file_path)
                
                if not os.path.exists(local_dir):
                    os.makedirs(local_dir)
                
                with open(local_file_path, 'wb') as f:
                    f.write(content)
                
                progress = int((i / max(len(to_copy), 1)) * 100)
                msg = ""
                if status == 'added':
                    msg = f"  [{progress:3d}%] ({i}/{total_files}) 新增: {file_path}"
                elif status == 'modified':
                    msg = f"  [{progress:3d}%] ({i}/{total_files}) 更新: {file_path}"
                elif status == 'renamed':
                    msg = f"  [{progress:3d}%] ({i}/{total_files}) 重命名: {file_path}"
                
                print(msg)
                self.log(msg.strip())
                success_count += 1
            else:
                fail_count += 1
                msg = f"  [{int(i/total_files*100):3d}%] ({i}/{total_files}) ❌ 复制失败: {file_path}"
                print(msg)
                self.log(msg.strip())
        
        if to_clear:
            removed_file_path = os.path.join(self.update_folder, "需要删除的文件.txt")
            with open(removed_file_path, 'w', encoding='utf-8') as f:
                for fp in to_clear:
                    f.write(f"{fp}\n")
            
            for j, file_path in enumerate(to_clear, 1):
                ext_lower = os.path.splitext(file_path)[1].lower()
                if ext_lower in ('.erb', '.erh'):
                    local_file_path = os.path.join(self.update_folder, file_path)
                    local_dir = os.path.dirname(local_file_path)
                    if not os.path.exists(local_dir):
                        os.makedirs(local_dir)
                    
                    self.log(f"检查是否需要保留: {file_path}")
                    content_removed = self.copy_file_from_git(file_path, branch)
                    
                    if content_removed is None:
                        open(local_file_path, 'w', encoding='utf-8').close()
                        msg = f"  [{int((len(to_copy)+j)/total_files*100):3d}%] 置空ERB/ERH: {file_path}"
                        print(msg)
                        self.log(msg.strip())
                    else:
                        with open(local_file_path, 'wb') as f:
                            f.write(content_removed)
                        msg = f"  [{int((len(to_copy)+j)/total_files*100):3d}%] 保留ERB/ERH: {file_path}"
                        print(msg)
                        self.log(msg.strip() + " (目标分支仍存在内容)")
                    success_count += 1
                else:
                    removed_files.append(file_path)
                    msg = f"  [{int((len(to_copy)+j)/total_files*100):3d}%] 标记删除: {file_path}"
                    print(msg)
                    self.log(msg.strip())
                    success_count += 1
        
        if removed_files:
            self.generate_delete_script(removed_files)
        
        self.log(f"更新完成. 成功: {success_count}, 失败: {fail_count}")
        self.log_file.close()
        
        print(f"\n✓ 复制完成！")
        print(f"  - 成功: {success_count} 个文件")
        print(f"  - 失败: {fail_count} 个文件")
        print(f"  - 保存位置: {self.update_folder}")
        print(f"  - 调试日志: {log_path}")
        
        self.generate_file_list(files_to_copy)
        
        return success_count > 0

    def log(self, message):
        if hasattr(self, 'log_file') and self.log_file:
            self.log_file.write(message + "\n")
            self.log_file.flush()

    def generate_delete_script(self, removed_files):
        """生成删除文件的批处理脚本"""
        script_path = os.path.join(self.update_folder, "一键删除旧文件.bat")
        
        try:
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write("@echo off\n")
                f.write("chcp 65001 >nul\n")
                
                f.write("echo ==========================================\n")
                f.write("echo      EraTW Magic DLC 一键删除旧文件脚本\n")
                f.write("echo ==========================================\n")
                f.write("echo.\n")
                f.write("echo 本脚本将自动把旧文件移动到备份文件夹中\n")
                f.write("echo 请确保本脚本在游戏根目录或更新文件夹中运行\n")
                f.write("echo.\n")
                f.write("pause\n\n")
                
                # 创建备份文件夹名称 (使用时间戳)
                f.write("set \"TIMESTAMP=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%\"\n")
                f.write("set \"TIMESTAMP=%TIMESTAMP: =0%\"\n")
                f.write("set \"BACKUP_ROOT=backup_deleted_%TIMESTAMP%\"\n\n")
                
                f.write("echo 创建备份文件夹: %BACKUP_ROOT%\n")
                f.write("if not exist \"%BACKUP_ROOT%\" mkdir \"%BACKUP_ROOT%\"\n\n")
                
                for file_path in removed_files:
                    # 转换路径分隔符
                    win_path = file_path.replace('/', '\\')
                    
                    f.write(f"if exist \"{win_path}\" (\n")
                    f.write(f"    echo [删除] {win_path}\n")
                    
                    # 创建目标目录结构
                    dir_name = os.path.dirname(win_path)
                    if dir_name:
                        f.write(f"    if not exist \"%BACKUP_ROOT%\\{dir_name}\" mkdir \"%BACKUP_ROOT%\\{dir_name}\" >nul\n")
                    
                    # 移动文件
                    f.write(f"    move \"{win_path}\" \"%BACKUP_ROOT%\\{win_path}\" >nul\n")
                    f.write(f") else (\n")
                    f.write(f"    echo [跳过] 文件不存在: {win_path}\n")
                    f.write(f")\n")
                
                f.write("\necho.\n")
                f.write("echo ==========================================\n")
                f.write("echo 操作完成！\n")
                f.write("echo 所有被删除的文件已移动到: %BACKUP_ROOT%\n")
                f.write("echo ==========================================\n")
                f.write("pause\n")
                
            print(f"  ✓ 已生成删除脚本: {script_path}")
        except Exception as e:
            print(f"  ❌ 生成删除脚本失败: {str(e)}")

    
    def generate_file_list(self, files_list):
        print("\n" + "="*60)
        print("生成文件变更列表")
        print("="*60)
        
        list_file_path = os.path.join(self.update_folder, "文件变更列表.txt")
        
        with open(list_file_path, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("文件变更列表\n")
            f.write("="*60 + "\n\n")
            
            added_files = [f for f in files_list if f['status'] == 'added']
            modified_files = [f for f in files_list if f['status'] == 'modified']
            removed_files = [f for f in files_list if f['status'] == 'removed']
            renamed_files = [f for f in files_list if f['status'] == 'renamed']
            
            f.write(f"【新增文件】({len(added_files)} 个)\n")
            f.write("-"*60 + "\n")
            for file_info in sorted(added_files, key=lambda x: x['filename']):
                f.write(f"+ {file_info['filename']}\n")
            
            f.write("\n")
            f.write(f"【修改文件】({len(modified_files)} 个)\n")
            f.write("-"*60 + "\n")
            for file_info in sorted(modified_files, key=lambda x: x['filename']):
                f.write(f"~ {file_info['filename']}\n")
            
            if renamed_files:
                f.write("\n")
                f.write(f"【重命名文件】({len(renamed_files)} 个)\n")
                f.write("-"*60 + "\n")
                for file_info in sorted(renamed_files, key=lambda x: x['filename']):
                    f.write(f"R {file_info['filename']}\n")
            
            if removed_files:
                f.write("\n")
                f.write(f"【删除文件】({len(removed_files)} 个)\n")
                f.write("-"*60 + "\n")
                for file_info in sorted(removed_files, key=lambda x: x['filename']):
                    f.write(f"- {file_info['filename']}\n")
            
            f.write("\n")
            f.write("="*60 + "\n")
            f.write(f"总计: {len(files_list)} 个文件变更\n")
            f.write(f"  - 新增: {len(added_files)} 个\n")
            f.write(f"  - 修改: {len(modified_files)} 个\n")
            f.write(f"  - 删除: {len(removed_files)} 个\n")
            if renamed_files:
                f.write(f"  - 重命名: {len(renamed_files)} 个\n")
            f.write("="*60 + "\n")
        
        print(f"  ✓ 文件列表已生成: {list_file_path}")
    
    def show_comparison(self):
        print("\n" + "="*60)
        print("分支信息对比")
        print("="*60)
        
        nightly_info = self.get_branch_info(self.nightly_branch)
        developing_info = self.get_branch_info(self.developing_branch)
        
        if nightly_info:
            print(f"\n📦 Nightly-Build 分支（最新版）:")
            print(f"   提交: {nightly_info['sha']}")
            print(f"   时间: {nightly_info['date']}")
            print(f"   说明: {nightly_info['message'][:50]}...")
        
        if developing_info:
            print(f"\n📦 Developing 分支（原始版本）:")
            print(f"   提交: {developing_info['sha']}")
            print(f"   时间: {developing_info['date']}")
            print(f"   说明: {developing_info['message'][:50]}...")
    
    def run(self):
        print("="*60)
        print("EraTW Magic DLC Git更新工具")
        print("="*60)
        print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n说明：本工具使用Git获取变更文件，快速且稳定")
        
        if not self.check_git_repository():
            input("\n按回车键退出...")
            return
        
        if not self.detect_remote_branches():
            input("\n按回车键退出...")
            return
        
        if not self.check_remote():
            print("\n⚠️  警告：未找到远程仓库")
            print("将尝试使用本地分支...")
        
        if not self.fetch_branches():
            print("\n⚠️  警告：获取远程分支失败")
            print("将尝试使用本地分支...")
        
        self.show_comparison()
        
        files_to_copy = self.get_changed_files(self.nightly_branch, self.developing_branch)
        
        if not files_to_copy:
            print("\n❌ 未找到变更文件")
            return
        
        print("\n" + "="*60)
        print("文件变更统计")
        print("="*60)
        
        added = sum(1 for f in files_to_copy if f['status'] == 'added')
        modified = sum(1 for f in files_to_copy if f['status'] == 'modified')
        removed = sum(1 for f in files_to_copy if f['status'] == 'removed')
        renamed = sum(1 for f in files_to_copy if f['status'] == 'renamed')
        
        print(f"\n新增: {added} 个")
        print(f"修改: {modified} 个")
        print(f"删除: {removed} 个")
        print(f"重命名: {renamed} 个")
        print(f"总计: {len(files_to_copy)} 个")
        
        print("\n" + "="*60)
        print("开始复制文件")
        print("="*60)
        print("注意：")
        print("  - 只复制有变更的文件")
        print("  - 文件将保存到 '更新文件' 文件夹")
        print("  - 您需要手动复制文件到游戏目录")
        print("  - 或者使用 '应用更新.bat' 自动应用")
        print()
        
        if self.copy_files_to_update_folder(files_to_copy, self.nightly_branch):
            print("\n" + "="*60)
            print("✓ 更新文件准备完成！")
            print("="*60)
            print(f"\n更新文件已保存到: {self.update_folder}")
            print("\n请按照以下步骤更新:")
            print("1. 打开 '更新文件' 文件夹")
            print("2. 将文件夹中的文件复制到游戏目录")
            print("3. 运行 '一键删除旧文件.bat' 自动备份并清理旧文件（如果有）")
            print("4. 完成后可以删除 '更新文件' 文件夹")
            print("\n或者运行 '应用更新.bat' 自动应用更新")
        else:
            print("\n❌ 复制文件失败")
        
        input("\n按回车键退出...")

if __name__ == "__main__":
    updater = GitUpdater()
    updater.run()
