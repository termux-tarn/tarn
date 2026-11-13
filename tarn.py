#!/usr/bin/env python3
import os
import sys
import json
import tarfile
import shutil
import urllib.request
from pathlib import Path

# Termux 环境变量 PREFIX
PREFIX = Path(os.environ.get("PREFIX", "/data/data/com.termux/files/usr"))
TARN_DB = PREFIX / "var" / "lib" / "tarn"
INSTALLED_DIR = TARN_DB / "installed"
LOCAL_INDEX = TARN_DB / "index.json"

# 默认的仓库源地址
REPO_URL = "https://termux-tarn.github.io/repo/index.json"

def init_db():
    """初始化 Tarn 的本地数据库目录"""
    INSTALLED_DIR.mkdir(parents=True, exist_ok=True)
    TARN_DB.mkdir(parents=True, exist_ok=True)

def get_installed(pkg_name):
    """检查包是否已安装"""
    meta_path = INSTALLED_DIR / f"{pkg_name}.json"
    if meta_path.exists():
        with open(meta_path, "r") as f:
            return json.load(f)
    return None

def update():
    """从远程拉取 index.json 索引"""
    print(f"Fetching index from {REPO_URL}...")
    try:
        urllib.request.urlretrieve(REPO_URL, LOCAL_INDEX)
        print("✅ Index updated successfully!")
    except Exception as e:
        print(f"❌ Failed to update index: {e}")

def install(pkg_source):
    """安装包（支持本地文件路径 或 远程包名）"""
    init_db()
    pkg_path = Path(pkg_source)
    is_temp_download = False

    # 1. 如果不是本地文件，说明是从仓库下载
    if not pkg_path.exists():
        if not LOCAL_INDEX.exists():
            print("❌ Index not found. Run 'tarn update' first.")
            return
        
        try:
            with open(LOCAL_INDEX, "r") as f:
                index_data = json.load(f)
        except json.JSONDecodeError:
            print("❌ Failed to parse index.json. Try 'tarn update' again.")
            return

        pkg_info = index_data.get("packages", {}).get(pkg_source)
        if not pkg_info:
            print(f"❌ Package '{pkg_source}' not found in index.")
            return

        download_url = pkg_info["url"]
        print(f"Downloading {pkg_source} from {download_url}...")
        
        # 下载到临时目录
        pkg_path = TARN_DB / f"{pkg_source}.tarn"
        try:
            urllib.request.urlretrieve(download_url, pkg_path)
            is_temp_download = True
        except Exception as e:
            print(f"❌ Download failed: {e}")
            return

    # 2. 开始解压并读取元数据
    print(f"Unpacking {pkg_path.name}...")
    temp_dir = TARN_DB / "tmp" / pkg_path.stem
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True)

    try:
        with tarfile.open(pkg_path, "r:gz") as tar:
            tar.extractall(path=temp_dir)
    except Exception as e:
        print(f"❌ Failed to unpack: {e}")
        return

    meta_file = temp_dir / "meta.json"
    if not meta_file.exists():
        print("❌ Invalid .tarn package (missing meta.json).")
        return
    
    with open(meta_file, "r") as f:
        meta = json.load(f)
    
    pkg_name = meta["name"]
    version = meta["version"]

    if get_installed(pkg_name):
        print(f"❌ Error: {pkg_name} is already installed. Remove it first.")
        return

    # 3. 复制文件
    print(f"Installing {pkg_name} v{version}...")
    files_dir = temp_dir / "files"
    installed_files = []
    
    if files_dir.exists():
        for root, dirs, files in os.walk(files_dir):
            for file in files:
                src_path = Path(root) / file
                rel_path = src_path.relative_to(files_dir)
                dest_path = PREFIX / rel_path
                
                # 确保目标目录存在
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                # 复制文件并保留权限
                shutil.copy2(src_path, dest_path)
                
                # 【修复 Bug】给 bin 目录下的文件自动加执行权限
                if str(rel_path).startswith("bin/"):
                    dest_path.chmod(0o755)
                
                installed_files.append(str(rel_path))
                print(f"  -> {rel_path}")

    # 4. 执行 post-install.sh (可选)
    post_script = temp_dir / "scripts" / "post-install.sh"
    if post_script.exists():
        print("Running post-install script...")
        os.environ["TARN_PREFIX"] = str(PREFIX)
        post_script.chmod(0o755)
        os.system(f"bash {post_script}")

    # 5. 记录到数据库
    meta["installed_files"] = installed_files
    with open(INSTALLED_DIR / f"{pkg_name}.json", "w") as f:
        json.dump(meta, f, indent=2)

    # 6. 清理临时文件
    shutil.rmtree(temp_dir)
    if is_temp_download and pkg_path.exists():
        pkg_path.unlink() # 删除下载的 .tarn 压缩包

    print(f"✅ Successfully installed {pkg_name}.")

def remove(pkg_name):
    """卸载包"""
    meta = get_installed(pkg_name)
    if not meta:
        print(f"❌ Error: {pkg_name} is not installed.")
        return

    print(f"Removing {pkg_name} v{meta['version']}...")
    
    # 删除文件
    for rel_path in meta.get("installed_files", []):
        dest_path = PREFIX / rel_path
        if dest_path.exists():
            dest_path.unlink()
            print(f"  <- removed {rel_path}")
    
    # 删除数据库记录
    (INSTALLED_DIR / f"{pkg_name}.json").unlink()
    print(f"✅ Successfully removed {pkg_name}.")

def list_pkgs():
    """列出已安装的包"""
    init_db()
    installed = list(INSTALLED_DIR.glob("*.json"))
    if not installed:
        print("No packages installed via Tarn.")
        return
    
    print(f"{'Package':<20} {'Version':<10}")
    print("-" * 30)
    for f in installed:
        with open(f, "r") as file:
            meta = json.load(file)
            print(f"{meta['name']:<20} {meta['version']:<10}")

def main():
    init_db()
    if len(sys.argv) < 2:
        print("Usage: tarn <install|remove|list|update> [args]")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "install" and len(sys.argv) == 3:
        install(sys.argv[2])
    elif cmd == "remove" and len(sys.argv) == 3:
        remove(sys.argv[2])
    elif cmd == "list":
        list_pkgs()
    elif cmd == "update":
        update()
    else:
        print("Invalid command or arguments.")
        print("Usage: tarn <install|remove|list|update>")

if __name__ == "__main__":
    main()