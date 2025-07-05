#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PPJF 完整配置工具
整合了原有 setup.py 的所有功能
"""

import json
import os
import sys
import shutil
import subprocess
import winreg
from pathlib import Path
from typing import Dict, Optional, List, Tuple

from ..core.launcher import PotPlayerLauncher


class PPJFConfigurator:
    def __init__(self):
        # 当前包的根目录 (src/jellypot/)
        self.package_root = Path(__file__).parent.parent.absolute()
        # 各个子目录
        self.config_dir = self.package_root / "config"
        self.scripts_dir = self.package_root / "scripts"
        self.assets_dir = self.package_root / "assets"
        
        self.config_file = self.config_dir / "config.json"
        self.config = self.load_config()
        
    def load_config(self) -> Dict:
        """加载配置文件"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 返回默认配置
            return {
                "jellyfin": {
                    "server_url": "http://localhost:8096",
                    "server_path": "C:\\Program Files\\Jellyfin\\Server",
                    "service_name": "JellyfinServer"
                },
                "potplayer": {
                    "executable_path": "C:\\Program Files\\DAUM\\PotPlayer\\PotPlayerMini64.exe",
                    "reg_file": "PotPlayerMini64.reg"
                },
                "browser": {
                    "executable_path": "C:\\Program Files\\LibreWolf\\librewolf.exe",
                    "process_name": "librewolf.exe",
                    "type": "LibreWolf"
                },
                "paths": {
                    "script_directory": str(self.scripts_dir),
                    "powershell_script": str(self.scripts_dir / "potplayer.ps1")
                },
                "userscripts": {
                    "potplayer_script": "OpenWithPotplayerUserscript.js",
                    "media_info_script": "OpenMediaInfoPathScriptmonkey.js"
                },
                "optional_features": {
                    "auto_start_stop_server": True,
                    "local_filesystem_links": False,
                    "fullscreen_mode": False,
                    "auto_fullscreen": False
                }
            }
    
    def save_config(self):
        """保存配置文件"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
        print(f"✅ 配置已保存到: {self.config_file}")
    
    def detect_software_paths(self) -> Dict[str, Optional[str]]:
        """自动检测软件安装路径"""
        detected = {}
        
        # 使用 PotPlayerLauncher 检测 PotPlayer
        launcher = PotPlayerLauncher()
        if Path(launcher.potplayer_path).exists():
            detected['potplayer'] = launcher.potplayer_path
        
        # 检测浏览器
        browser_paths = {
            'LibreWolf': [
                "C:\\Program Files\\LibreWolf\\librewolf.exe",
                "C:\\Program Files (x86)\\LibreWolf\\librewolf.exe"
            ],
            'Firefox': [
                "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
                "C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"
            ],
            'Chrome': [
                "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
            ]
        }
        
        for browser_type, paths in browser_paths.items():
            for path in paths:
                if os.path.exists(path):
                    detected['browser'] = path
                    detected['browser_type'] = browser_type
                    detected['browser_process'] = Path(path).name.lower()
                    break
            if 'browser' in detected:
                break
        
        # 检测 Jellyfin
        jellyfin_paths = [
            "C:\\Program Files\\Jellyfin\\Server",
            "C:\\Program Files (x86)\\Jellyfin\\Server"
        ]
        
        for path in jellyfin_paths:
            if os.path.exists(path):
                detected['jellyfin'] = path
                break
        
        return detected
    
    def print_banner(self):
        """打印欢迎横幅"""
        print("=" * 60)
        print("🎬 PPJF 自动配置工具")
        print("   Jellyfin + PotPlayer 整合配置")
        print("=" * 60)
        print()
    
    def show_detected_software(self, detected: Dict):
        """显示检测到的软件"""
        print("🔍 自动检测结果:")
        print("-" * 40)
        
        if 'potplayer' in detected:
            print(f"✅ PotPlayer: {detected['potplayer']}")
        else:
            print("❌ PotPlayer: 未检测到")
        
        if 'browser' in detected:
            print(f"✅ 浏览器: {detected['browser']} ({detected['browser_type']})")
        else:
            print("❌ 浏览器: 未检测到支持的浏览器")
        
        if 'jellyfin' in detected:
            print(f"✅ Jellyfin: {detected['jellyfin']}")
        else:
            print("❌ Jellyfin: 未检测到")
        
        print()
    
    def get_user_input(self, prompt: str, default: str = "") -> str:
        """获取用户输入，并去除首尾引号"""
        if default:
            user_input = input(f"{prompt} [默认: {default}]: ").strip()
            value = user_input if user_input else default
        else:
            value = input(f"{prompt}: ").strip()
        # 去除首尾引号
        return value.strip('"\'')
    
    def update_registry_file_for_exe(self, exe_path: str):
        """更新注册表文件，使用 exe 启动器而不是 PowerShell"""
        print("📝 更新注册表文件为 exe 启动器...")
        
        reg_file = self.config_dir / self.config['potplayer']['reg_file']
        
        content = f"""Windows Registry Editor Version 5.00
[HKEY_CLASSES_ROOT\\potplayer]
@="URL:potplayer protocol"
"URL Protocol"=""
[HKEY_CLASSES_ROOT\\potplayer\\shell]
[HKEY_CLASSES_ROOT\\potplayer\\shell\\open]
[HKEY_CLASSES_ROOT\\potplayer\\shell\\open\\command]
@="\\"{exe_path}\\" %1"
"""
        
        with open(reg_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 注册表已更新为 exe 启动器: {reg_file}")
    
    def create_batch_launcher(self):
        """创建批处理启动器"""
        print("📝 创建 Jellyfin 批处理启动器...")
        
        batch_file = self.scripts_dir / "Jellyfin.bat"
        
        batch_content = f"""@echo off
tasklist /FI "IMAGENAME eq jellyfin.exe" 2>NUL | find /I "jellyfin.exe" >NUL
if errorlevel 1 (
    net start {self.config['jellyfin']['service_name']}
)

:waitForServer
curl -s {self.config['jellyfin']['server_url']} > nul
if %errorlevel% neq 0 (
    ping -n 1 -w 100 127.0.0.1 > nul 
    goto waitForServer
)

start "" "{self.config['browser']['executable_path']}" "{self.config['jellyfin']['server_url']}/web/index.html#/home.html"

:LOOP
tasklist | find /i "jellyfin.exe" >nul
IF ERRORLEVEL 1 (
    net start {self.config['jellyfin']['service_name']}
)

tasklist | find /i "{self.config['browser']['process_name']}" >nul
IF ERRORLEVEL 1 GOTO EXECUTE
timeout /t 1 >nul
GOTO LOOP

:EXECUTE
net stop {self.config['jellyfin']['service_name']}
exit
"""
        
        with open(batch_file, 'w', encoding='utf-8') as f:
            f.write(batch_content)
        
        print(f"✅ 已创建: {batch_file}")
    
    def interactive_setup(self):
        """交互式配置"""
        print("🛠️  开始交互式配置...")
        print()
        
        detected = self.detect_software_paths()
        self.show_detected_software(detected)
        
        # Jellyfin 配置
        print("📡 Jellyfin 配置:")
        self.config['jellyfin']['server_url'] = self.get_user_input(
            "Jellyfin 服务器 URL", 
            self.config['jellyfin']['server_url']
        )
        
        if 'jellyfin' in detected:
            self.config['jellyfin']['server_path'] = detected['jellyfin']
        else:
            self.config['jellyfin']['server_path'] = self.get_user_input(
                "Jellyfin 服务器安装路径",
                self.config['jellyfin']['server_path']
            )
        print()
        
        # PotPlayer 配置
        print("🎥 PotPlayer 配置:")
        if 'potplayer' in detected:
            self.config['potplayer']['executable_path'] = detected['potplayer']
        else:
            self.config['potplayer']['executable_path'] = self.get_user_input(
                "PotPlayer 可执行文件路径",
                self.config['potplayer']['executable_path']
            )
        print()
        
        # 浏览器配置
        print("🌐 浏览器配置:")
        if 'browser' in detected:
            self.config['browser']['executable_path'] = detected['browser']
            self.config['browser']['type'] = detected['browser_type']
            self.config['browser']['process_name'] = detected['browser_process']
        else:
            self.config['browser']['executable_path'] = self.get_user_input(
                "浏览器可执行文件路径",
                self.config['browser']['executable_path']
            )
            self.config['browser']['type'] = self.get_user_input(
                "浏览器类型 (LibreWolf/Firefox/Chrome)",
                self.config['browser']['type']
            )
            self.config['browser']['process_name'] = Path(
                self.config['browser']['executable_path']
            ).name.lower()
        print()
        
        # 可选功能
        print("🔧 可选功能配置:")
        self.config['optional_features']['auto_start_stop_server'] = input(
            "启用自动启动/停止 Jellyfin 服务器? (y/n) [默认: y]: "
        ).lower() != 'n'
        
        self.config['optional_features']['local_filesystem_links'] = input(
            "启用本地文件夹链接功能? (y/n) [默认: n]: "
        ).lower() == 'y'
        
        self.config['optional_features']['fullscreen_mode'] = input(
            "启用全屏模式? (y/n) [默认: n]: "
        ).lower() == 'y'
        
        print()

    def validate_paths(self) -> bool:
        """验证配置的路径是否有效"""
        print("🔍 验证配置路径...")
        errors = []
        
        # 验证 PotPlayer
        if not os.path.exists(self.config['potplayer']['executable_path']):
            errors.append(f"PotPlayer 路径无效: {self.config['potplayer']['executable_path']}")
        
        # 验证浏览器
        if not os.path.exists(self.config['browser']['executable_path']):
            errors.append(f"浏览器路径无效: {self.config['browser']['executable_path']}")
        
        if errors:
            print("❌ 发现配置错误:")
            for error in errors:
                print(f"   {error}")
            return False
        
        print("✅ 所有路径验证通过")
        return True

    def update_powershell_script(self):
        """更新 PowerShell 脚本"""
        print("📝 更新 potplayer.ps1...")
        
        ps_file = self.scripts_dir / "potplayer.ps1"
        
        ps_content = f"""Add-Type -Assembly System.Web

# 从参数获取路径
$path = $args[0]
$path = $path -replace "potplayer://" , ""

# 解码 URL
$path = $path -replace "\\+", "%2B"
$path = [System.Web.HttpUtility]::UrlDecode($path)

# 清理斜杠和反斜杠
$path = $path -replace "///", "\\\\"
$path = $path -replace "\\\\\\\\", "\\\\"
$path = $path -replace "\\\\", "\\\\"
$path = $path -replace "//", "\\\\"

# 修正所有磁盘驱动器路径
$path = $path -replace "^([A-Z]):\\\\", '$1:\\'
$path = $path -replace "^([A-Z])/", '$1:\\'
$path = $path -replace "^([A-Z]):", '$1:\\'

# 替换特定的 \\\\?\\ 路径格式
$path = $path -replace "([A-Z]):\\\\\\\\\\?\\\\", '$1:\\'
$path = $path -replace "\\\\\\\\\\?\\\\", "\\\\"

# 将所有剩余的斜杠规范化为反斜杠
$path = $path -replace "/", "\\\\"

Write-Host "标准化路径: $path"
# 使用标准化路径启动 PotPlayer
& "{self.config['potplayer']['executable_path']}" $path
"""
        
        with open(ps_file, 'w', encoding='utf-8') as f:
            f.write(ps_content)
        
        print(f"✅ 已更新: {ps_file}")

    def run(self):
        """运行配置程序"""
        self.print_banner()
        
        # 交互式设置
        self.interactive_setup()
        
        # 验证路径
        if not self.validate_paths():
            print("❌ 路径验证失败，请检查配置后重试")
            return False
        
        # 保存配置
        self.save_config()
        
        # 更新文件
        print()
        print("🔄 更新配置文件...")
        self.create_batch_launcher()
        self.update_powershell_script()
        
        print()
        print("🎉 配置完成!")
        print("=" * 60)
        print("📋 后续步骤:")
        print("1. 运行 uv run python -m jellypot.core.build 构建 exe")
        print("2. 导入注册表文件启用 potplayer:// 协议")
        print("3. 测试配置是否正常工作")
        
        return True


def main():
    """命令行入口函数"""
    configurator = PPJFConfigurator()
    # 这里可以添加配置逻辑
    print("PPJF 配置器已初始化")


if __name__ == "__main__":
    main()
