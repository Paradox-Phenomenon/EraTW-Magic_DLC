import os
import json
import requests
import shutil
from datetime import datetime
from pathlib import Path

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
