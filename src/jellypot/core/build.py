#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JellyPot 构建模块
用于构建 PotPlayer 启动器 exe
"""

import subprocess
import sys
from pathlib import Path


def install_dependencies():
    """安装构建所需的依赖"""
    print("📦 安装构建依赖...")
    try:
        # 去掉 --user 参数，确保在虚拟环境中正确安装
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', 'pyinstaller>=5.0'
        ])
        print("✅ 构建依赖安装成功")
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建依赖安装失败: {e}")
        sys.exit(1)


def build_exe():
    """构建 PotPlayer 启动器 exe"""
    print("🔨 构建 PotPlayer 启动器...")
    
    # 当前包根目录
    package_root = Path(__file__).parent.parent.absolute()
    project_root = package_root.parent.parent.absolute()
    
    # 入口文件
    entry_file = package_root / "__main__.py"
    
    if not entry_file.exists():
        print(f"❌ 入口文件不存在: {entry_file}")
        return None
    
    # PyInstaller 命令
    cmd = [
        "pyinstaller",
        "--onefile",                           # 单文件
        "--windowed",                          # 无控制台窗口
        "--name=potplayer_launcher",           # 输出文件名
        "--distpath=dist",                     # 输出目录
        "--workpath=build",                    # 临时目录
        "--specpath=.",                        # spec 文件目录
        "--clean",                             # 清理旧文件
        str(entry_file)                        # 入口文件
    ]
    
    try:
        subprocess.run(cmd, check=True, cwd=project_root)
        print("✅ exe 构建成功!")
        
        exe_path = project_root / "dist" / "potplayer_launcher.exe"
        if exe_path.exists():
            print(f"📁 exe 文件位置: {exe_path}")
            print(f"📏 文件大小: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
            
            # 更新注册表文件
            from ..config.configurator import PPJFConfigurator
            configurator = PPJFConfigurator()
            configurator.update_registry_file_for_exe(str(exe_path))
            
            return str(exe_path)
        else:
            print("❌ exe 文件未找到")
            return None
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        return None
        print(f"❌ 构建依赖安装失败: {e}")
        return False


def build_exe_launcher() -> str:
    """使用 PyInstaller 构建 exe"""
    print("🔨 构建 exe 文件...")

    # 项目根目录
    project_root = Path(__file__).parent.parent.parent.absolute()
    launcher_script = project_root / "src" / "jellypot" / "__main__.py"

    # 确保构建依赖已安装
    install_dependencies()

    # PyInstaller 命令
    cmd = [
        "pyinstaller",
        "--onefile",                                    # 单文件
        "--windowed",                                   # 无控制台窗口
        "--name=potplayer_launcher",                    # 输出文件名
        "--distpath=dist",                              # 输出目录
        "--workpath=build",                             # 临时目录
        "--specpath=.",                                 # spec 文件目录
        "--clean",                                      # 清理旧文件
        str(launcher_script)                              # 入口文件
    ]

    try:
        subprocess.run(cmd, check=True, cwd=project_root)
        print("✅ exe 构建成功!")

        exe_path = project_root / "dist" / "potplayer_launcher.exe"
        if exe_path.exists():
            print(f"📁 exe 文件位置: {exe_path}")
            print(f"📏 文件大小: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
            return str(exe_path)
        else:
            print("❌ exe 文件未找到")
            return None

    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        return None


def main():
    """主函数"""
    print("🚀 JellyPot 构建工具")
    print("=" * 50)
    
    exe_path = build_exe_launcher()
    if exe_path:
        print("\n🎉 构建完成!")
        print("=" * 50)
        print(f"📁 exe 文件: {exe_path}")
        print("📋 后续步骤:")
        print("1. 双击导入 PotPlayerMini64.reg 注册表文件")
        print("2. 测试 potplayer:// 协议是否正常工作")
        print("3. 在浏览器中测试 Jellyfin + PotPlayer 整合")


if __name__ == "__main__":
    main()
