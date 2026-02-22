import os
import sys
import subprocess
import shutil
import urllib.request
from datetime import datetime
from pathlib import Path

def install_pip():
    print("\n检查pip...")
    
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            timeout=10
        )
        print("✓ pip已安装")
        return True
    except:
        print("❌ pip未找到")
        print("\n正在尝试自动安装pip...")
        
        try:
            get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
            print(f"下载get-pip.py...")
            
            with urllib.request.urlopen(get_pip_url, timeout=30) as response:
                get_pip_content = response.read()
            
            get_pip_path = os.path.join(os.path.dirname(sys.executable), "get-pip.py")
            with open(get_pip_path, 'wb') as f:
                f.write(get_pip_content)
            
            print("运行get-pip.py安装pip...")
            result = subprocess.run(
                [sys.executable, get_pip_path],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                print("✓ pip安装成功")
                os.remove(get_pip_path)
                return True
            else:
                print("❌ pip安装失败")
                print(f"错误信息：{result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ pip安装过程出错: {str(e)}")
            print("\n请手动安装pip：")
            print("1. 访问: https://bootstrap.pypa.io/get-pip.py")
            print("2. 保存为get-pip.py")
            print(f"3. 运行: {sys.executable} get-pip.py")
            return False

def check_and_install_dependencies():
    print("检查依赖库...")
    print(f"当前Python路径: {sys.executable}")
    print(f"当前Python版本: {sys.version}")
    
    try:
        import requests
        print("✓ requests库已安装")
        return True
    except ImportError:
        print("❌ requests库未找到")
        
        if not install_pip():
            input("\n按回车键退出...")
            sys.exit(1)
        
        print("\n正在尝试自动安装requests库...")
        print(f"使用Python: {sys.executable}")
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "requests"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            print(f"安装返回码: {result.returncode}")
            if result.stdout:
                print(f"输出: {result.stdout[-200:]}")
            if result.stderr:
                print(f"错误: {result.stderr[-200:]}")
            
            if result.returncode == 0:
                print("✓ requests库安装成功")
                print("\n请重新运行程序")
                return False
            else:
                print("❌ requests库安装失败")
                print(f"\n完整错误信息：")
                print(result.stderr)
                print("\n可能的原因：")
                print("1. pip未安装或未添加到PATH")
                print("2. 网络连接问题")
                print("3. 权限不足")
                print("4. 多个Python版本冲突")
                print("\n请尝试以下方法：")
                print("\n方法1：使用国内镜像安装")
                print(f"  {sys.executable} -m pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple")
                print("\n方法2：手动下载并安装")
                print("  访问: https://pypi.org/project/requests/")
                print("  下载requests-*.whl文件")
                print(f"  运行: {sys.executable} -m pip install requests-*.whl")
                print("\n方法3：使用管理员权限运行")
                print("  右键点击bat文件，选择'以管理员身份运行'")
                print("\n方法4：检查Python版本")
                print(f"  当前Python: {sys.executable}")
                print("  请确认这是您想使用的Python版本")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ 安装超时（60秒）")
            print("\n可能的原因：")
            print("1. 网络连接缓慢")
            print("2. pip源响应慢")
            print("\n建议：")
            print("  使用国内镜像：")
            print(f"  {sys.executable} -m pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple")
            return False
        except FileNotFoundError:
            print("❌ 未找到pip")
            print(f"\nPython路径：{sys.executable}")
            print("\n请检查：")
            print("1. Python是否正确安装")
            print("2. pip是否包含在Python安装包中")
            print("\n手动安装pip：")
            print("  访问: https://bootstrap.pypa.io/get-pip.py")
            print("  下载get-pip.py")
            print(f"  运行: {sys.executable} get-pip.py")
            return False
        except Exception as e:
            print(f"❌ 安装过程出错: {type(e).__name__}")
            print(f"错误详情: {str(e)}")
            print("\n请尝试手动安装：")
            print(f"  {sys.executable} -m pip install requests")
            return False

if not check_and_install_dependencies():
    input("\n按回车键退出...")
    sys.exit(1)

import requests

class GitHubUpdaterNoGit:
    def __init__(self):
        self.repo_owner = "Paradox-Phenomenon"
        self.repo_name = "EraTW-Magic_DLC"
        self.nightly_branch = "nightly-build"
        self.developing_branch = "developing"
        self.api_base = "https://api.github.com"
        self.raw_base = "https://raw.githubusercontent.com"
        self.repo_path = os.path.dirname(os.path.abspath(__file__))
        self.update_folder = os.path.join(self.repo_path, "更新文件")
        
    def make_api_request(self, endpoint):
        try:
            url = f"{self.api_base}{endpoint}"
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API请求失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"请求错误: {str(e)}")
            return None
    
    def check_network_connection(self):
        print("\n检查网络连接...")
        try:
            response = requests.get("https://api.github.com", timeout=10)
            if response.status_code == 200:
                print("✓ 网络连接正常")
                return True
            else:
                print("❌ 无法连接到GitHub")
                return False
        except Exception as e:
            print(f"❌ 网络连接失败: {str(e)}")
            return False
    
    def get_branch_info(self, branch):
        endpoint = f"/repos/{self.repo_owner}/{self.repo_name}/branches/{branch}"
        data = self.make_api_request(endpoint)
        if data and 'commit' in data:
            return {
                'sha': data['commit']['sha'][:7],
                'date': data['commit']['commit']['committer']['date'][:19].replace('T', ' '),
                'message': data['commit']['commit']['message']
            }
        return None
    
    def get_commits_between_branches(self, branch1, branch2):
        endpoint = f"/repos/{self.repo_owner}/{self.repo_name}/compare/{branch2}...{branch1}"
        data = self.make_api_request(endpoint)
        if data and 'commits' in data:
            commits = []
            for commit in data['commits']:
                commits.append({
                    'sha': commit['sha'][:7],
                    'date': commit['commit']['committer']['date'][:19].replace('T', ' '),
                    'message': commit['commit']['message']
                })
            return commits
        return []
    
    def get_files_between_branches(self, branch1, branch2):
        endpoint = f"/repos/{self.repo_owner}/{self.repo_name}/compare/{branch2}...{branch1}"
        data = self.make_api_request(endpoint)
        if data and 'files' in data:
            return data['files']
        return []
    
    def download_file(self, file_path, branch):
        raw_url = f"{self.raw_base}/{self.repo_owner}/{self.repo_name}/{branch}/{file_path}"
        try:
            response = requests.get(raw_url, timeout=30)
            if response.status_code == 200:
                return response.content
            else:
                print(f"  ❌ 下载失败: {file_path} (状态码: {response.status_code})")
                return None
        except Exception as e:
            print(f"  ❌ 下载错误: {file_path} ({str(e)})")
            return None
    
    def download_files_to_update_folder(self, files_to_download, branch):
        print(f"\n准备下载文件到更新文件夹...")
        
        if os.path.exists(self.update_folder):
            shutil.rmtree(self.update_folder)
        os.makedirs(self.update_folder)
        
        total_files = len(files_to_download)
        success_count = 0
        fail_count = 0
        
        print(f"共需下载 {total_files} 个文件\n")
        
        for i, file_info in enumerate(files_to_download, 1):
            file_path = file_info['filename']
            status = file_info['status']
            
            if status == 'removed':
                removed_file_path = os.path.join(self.update_folder, "需要删除的文件.txt")
                with open(removed_file_path, 'a', encoding='utf-8') as f:
                    f.write(f"{file_path}\n")
                print(f"  [{int(i/total_files*100):3d}%] ({i}/{total_files}) 标记删除: {file_path}")
                success_count += 1
                continue
            
            content = self.download_file(file_path, branch)
            if content:
                local_file_path = os.path.join(self.update_folder, file_path)
                local_dir = os.path.dirname(local_file_path)
                
                if not os.path.exists(local_dir):
                    os.makedirs(local_dir)
                
                with open(local_file_path, 'wb') as f:
                    f.write(content)
                
                progress = int((i / total_files) * 100)
                if status == 'added':
                    print(f"  [{progress:3d}%] ({i}/{total_files}) 新增: {file_path}")
                elif status == 'modified':
                    print(f"  [{progress:3d}%] ({i}/{total_files}) 更新: {file_path}")
                elif status == 'renamed':
                    print(f"  [{progress:3d}%] ({i}/{total_files}) 重命名: {file_path}")
                
                success_count += 1
            else:
                fail_count += 1
        
        print(f"\n✓ 下载完成！")
        print(f"  - 成功: {success_count} 个文件")
        print(f"  - 失败: {fail_count} 个文件")
        print(f"  - 保存位置: {self.update_folder}")
        
        return success_count > 0
    
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
        
        print("\n" + "="*60)
        print("Nightly-Build 相比 Developing 的变更")
        print("="*60)
        
        commits = self.get_commits_between_branches(self.nightly_branch, self.developing_branch)
        if commits:
            print(f"\n共有 {len(commits)} 个新提交:\n")
            for i, commit in enumerate(commits[:10], 1):
                print(f"{i}. [{commit['sha']}] {commit['date']}")
                print(f"   {commit['message']}")
            if len(commits) > 10:
                print(f"\n... 还有 {len(commits) - 10} 个提交")
        else:
            print("\n没有新的提交")
        
        files = self.get_files_between_branches(self.nightly_branch, self.developing_branch)
        if files:
            print(f"\n文件变更统计:")
            print(f"   修改: {len([f for f in files if f['status'] == 'modified'])} 个")
            print(f"   新增: {len([f for f in files if f['status'] == 'added'])} 个")
            print(f"   删除: {len([f for f in files if f['status'] == 'removed'])} 个")
        
        print("\n" + "="*60)
    
    def download_to_update_folder(self):
        print("\n开始下载差异文件...")
        
        files_to_download = self.get_files_between_branches(self.nightly_branch, self.developing_branch)
        if not files_to_download:
            print("❌ 无法获取文件变更信息")
            return False
        
        print(f"\n检测到 {len(files_to_download)} 个文件变更")
        
        if self.download_files_to_update_folder(files_to_download, self.nightly_branch):
            print("\n" + "="*60)
            print("✓ 下载成功！")
            print("="*60)
            print(f"\n更新文件已保存到: {self.update_folder}")
            print("\n请按照以下步骤手动更新:")
            print("1. 打开 '更新文件' 文件夹")
            print("2. 将文件夹中的文件复制到游戏目录")
            print("3. 如果有 '需要删除的文件.txt'，请删除其中列出的文件")
            print("4. 完成后可以删除 '更新文件' 文件夹")
            return True
        else:
            print("\n❌ 下载失败")
            return False
    
    def run(self):
        print("="*60)
        print("EraTW Magic DLC 自动更新工具（无Git版本）")
        print("="*60)
        print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if not self.check_network_connection():
            return
        
        nightly_info = self.get_branch_info(self.nightly_branch)
        developing_info = self.get_branch_info(self.developing_branch)
        
        if not nightly_info:
            print(f"\n❌ 无法获取 {self.nightly_branch} 分支信息")
            return
        
        if not developing_info:
            print(f"\n❌ 无法获取 {self.developing_branch} 分支信息")
            return
        
        self.show_comparison()
        
        print("\n开始自动下载差异文件...")
        print("注意：")
        print("  - 只下载有变更的文件，节省时间和带宽")
        print("  - 文件将保存到 '更新文件' 文件夹")
        print("  - 您需要手动复制文件到游戏目录")
        print()
        
        self.download_to_update_folder()

if __name__ == "__main__":
    try:
        updater = GitHubUpdaterNoGit()
        updater.run()
    except KeyboardInterrupt:
        print("\n\n程序已中断")
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
    
    input("\n按回车键退出...")
