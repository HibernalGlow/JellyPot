#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PPJF 自动配置工具
Jellyfin + PotPlayer 整合配置脚本

此脚本自动检测系统中的软件安装路径，并配置所有必要的文件。
"""

import json
import os
import sys
import shutil
import subprocess
import winreg
from pathlib import Path
from typing import Dict, Optional, List, Tuple

class PPJFConfigurator:
    def __init__(self):
        self.script_dir = Path(__file__).parent.absolute()
        self.config_file = self.script_dir / "config.json"
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
                    "script_directory": str(self.script_dir),
                    "powershell_script": str(self.script_dir / "potplayer.ps1")
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
        
        # 检测 PotPlayer
        potplayer_paths = [
            "C:\\Program Files\\DAUM\\PotPlayer\\PotPlayerMini64.exe",
            "C:\\Program Files (x86)\\DAUM\\PotPlayer\\PotPlayerMini64.exe",
            "C:\\Program Files\\PotPlayer\\PotPlayerMini64.exe",
            "C:\\Program Files (x86)\\PotPlayer\\PotPlayerMini64.exe"
        ]
        
        for path in potplayer_paths:
            if os.path.exists(path):
                detected['potplayer'] = path
                break
        
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
        
        # 脚本目录配置
        print("📁 脚本目录配置:")
        self.config['paths']['script_directory'] = self.get_user_input(
            "脚本目录路径",
            str(self.script_dir)
        )
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
        """验证配置的路径是否有效，并去除首尾引号"""
        print("🔍 验证配置路径...")
        errors = []
        
        # 更新脚本目录路径到当前实际目录
        self.config['paths']['script_directory'] = str(self.script_dir)
        self.config['paths']['powershell_script'] = str(self.script_dir / "potplayer.ps1")
        
        # 去除路径首尾引号
        self.config['potplayer']['executable_path'] = self.config['potplayer']['executable_path'].strip('"\'')
        self.config['browser']['executable_path'] = self.config['browser']['executable_path'].strip('"\'')
        self.config['paths']['script_directory'] = self.config['paths']['script_directory'].strip('"\'')
        
        # 验证 PotPlayer
        if not os.path.exists(self.config['potplayer']['executable_path']):
            errors.append(f"PotPlayer 路径无效: {self.config['potplayer']['executable_path']}")
        
        # 验证浏览器
        if not os.path.exists(self.config['browser']['executable_path']):
            errors.append(f"浏览器路径无效: {self.config['browser']['executable_path']}")
        
        # 验证脚本目录
        if not os.path.exists(self.config['paths']['script_directory']):
            errors.append(f"脚本目录无效: {self.config['paths']['script_directory']}")
        
        if errors:
            print("❌ 发现配置错误:")
            for error in errors:
                print(f"   {error}")
            return False
        
        print("✅ 所有路径验证通过")
        return True
    
    def update_batch_file(self):
        """更新批处理文件"""
        print("📝 更新 Jellyfin.bat...")
        
        batch_file = self.script_dir / "Jellyfin.bat"
        
        batch_content = f"""@echo off

tasklist /FI "IMAGENAME eq jellyfin.exe" 2>NUL | find /I "jellyfin.exe" >NUL
if errorlevel 1 (
    net start {self.config['jellyfin']['service_name']}
)

:waitForServer
tasklist /FI "IMAGENAME eq jellyfin.exe" 2>NUL | find /I "jellyfin.exe" >NUL
if errorlevel 1 (
    net start {self.config['jellyfin']['service_name']}
)

curl -s {self.config['jellyfin']['server_url']} > nul
if %errorlevel% neq 0 (ping -n 1 -w 100 127.0.0.1 > nul & goto waitForServer)
start "" "{self.config['browser']['executable_path']}" -url "{self.config['jellyfin']['server_url']}/web/index.html#/home.html"

:EXECUTEserv
tasklist /FI "IMAGENAME eq jellyfin.exe" 2>NUL | find /I "jellyfin.exe" >NUL
if errorlevel 1 (
    net start {self.config['jellyfin']['service_name']}
)

timeout /t 1 >nul

:LOOP

tasklist | find /i "jellyfin.exe" >nul
IF ERRORLEVEL 1 GOTO EXECUTEserv
timeout /t 1 >nul


tasklist | find /i "{self.config['browser']['process_name']}" >nul
IF ERRORLEVEL 1 GOTO EXECUTE
timeout /t 1 >nul
GOTO LOOP

:EXECUTE
net stop {self.config['jellyfin']['service_name']}
timeout /t 1 >nul
net stop {self.config['jellyfin']['service_name']}
exit
"""
        
        with open(batch_file, 'w', encoding='utf-8') as f:
            f.write(batch_content)
        
        print(f"✅ 已更新: {batch_file}")
    
    def update_powershell_script(self):
        """更新 PowerShell 脚本"""
        print("📝 更新 potplayer.ps1...")
        
        ps_file = self.script_dir / "potplayer.ps1"
        
        ps_content = f"""Add-Type -Assembly System.Web

# 从参数获取路径
$path = $args[0]
$path = $path -replace "potplayer://" , ""

# 解码 URL
$path = $path -replace "\\+", "%2B"
$path = [System.Web.HttpUtility]::UrlDecode($path)

# 清理斜杠和反斜杠
$path = $path -replace "///", "\\"
$path = $path -replace "\\\\\\\\", "\\"
$path = $path -replace "\\\\", "\\"
$path = $path -replace "//", "\\"

# 修正所有磁盘驱动器路径
$path = $path -replace "^([A-Z]):\\\\", '$1:\\'
$path = $path -replace "^([A-Z])/", '$1:\\'
$path = $path -replace "^([A-Z]):", '$1:\\'

# 替换特定的 \\\\?\\ 路径格式
$path = $path -replace "([A-Z]):\\\\\\\\\\?\\\\", '$1:\\'
$path = $path -replace "\\\\\\\\\\?\\\\", "\\"

# 将所有剩余的斜杠规范化为反斜杠
$path = $path -replace "/", "\\"

Write-Host "标准化路径: $path"
# 使用标准化路径启动 PotPlayer
& "{self.config['potplayer']['executable_path']}" $path
"""
        
        with open(ps_file, 'w', encoding='utf-8') as f:
            f.write(ps_content)
        
        print(f"✅ 已更新: {ps_file}")
    
    def update_userscripts(self):
        """更新用户脚本"""
        print("📝 更新用户脚本...")
        
        # 更新 PotPlayer 用户脚本
        potplayer_script = self.script_dir / self.config['userscripts']['potplayer_script']
        
        if potplayer_script.exists():
            with open(potplayer_script, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 替换 URL
            content = content.replace(
                "http://localhost:8096", 
                self.config['jellyfin']['server_url']
            )
            
            with open(potplayer_script, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 已更新: {potplayer_script}")
        
        # 更新媒体信息脚本
        media_script = self.script_dir / self.config['userscripts']['media_info_script']
        
        if media_script.exists():
            with open(media_script, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 替换 URL
            content = content.replace(
                "http://localhost:8096", 
                self.config['jellyfin']['server_url']
            )
            
            with open(media_script, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 已更新: {media_script}")
    
    def apply_registry_settings(self):
        """应用注册表设置"""
        print("📝 应用 PotPlayer 注册表设置...")
        
        reg_file = self.script_dir / self.config['potplayer']['reg_file']
        
        if reg_file.exists():
            try:
                subprocess.run(['regedit', '/s', str(reg_file)], check=True)
                print("✅ 注册表设置已应用")
            except subprocess.CalledProcessError:
                print("❌ 应用注册表设置失败，请手动运行 PotPlayerMini64.reg")
        else:
            print(f"❌ 注册表文件不存在: {reg_file}")
    
    def create_shortcuts(self):
        """创建快捷方式"""
        print("🔗 创建快捷方式...")
        
        # 这里可以添加创建桌面快捷方式的代码
        # 由于复杂性，暂时跳过，用户可以手动创建
        print("ℹ️  快捷方式创建请参考说明文档手动完成")
    
    def update_task_scheduler_xml(self):
        """更新任务计划程序 XML 文件"""
        print("📝 更新 JellyfinUAC.xml...")
        
        xml_file = self.script_dir / "JellyfinUAC.xml"
        
        if xml_file.exists():
            with open(xml_file, 'r', encoding='utf-16') as f:
                content = f.read()
            
            # 替换批处理文件路径
            old_path = "C:\\ProgramData\\PotPlayerJellyfin\\Jellyfin.bat"
            new_path = str(self.script_dir / "Jellyfin.bat").replace("\\", "\\\\")
            
            content = content.replace(old_path, new_path)
            
            with open(xml_file, 'w', encoding='utf-16') as f:
                f.write(content)
            
            print(f"✅ 已更新: {xml_file}")
        else:
            print(f"❌ 任务计划文件不存在: {xml_file}")
    
    def show_next_steps(self):
        """显示后续步骤"""
        print()
        print("🎉 配置完成!")
        print("=" * 60)
        print("📋 后续步骤:")
        print()
        print("1. 安装浏览器扩展:")
        if self.config['browser']['type'] in ['LibreWolf', 'Firefox']:
            print("   - ViolentMonkey: https://addons.mozilla.org/firefox/addon/violentmonkey/")
            if self.config['optional_features']['local_filesystem_links']:
                print("   - Local Filesystem Links: https://addons.mozilla.org/firefox/addon/local-filesystem-links/")
            if self.config['optional_features']['auto_fullscreen']:
                print("   - Auto Fullscreen: https://addons.mozilla.org/firefox/addon/autofullscreen/")
        
        print()
        print("2. 在 ViolentMonkey 中添加脚本:")
        print(f"   - {self.config['userscripts']['potplayer_script']}")
        if self.config['optional_features']['local_filesystem_links']:
            print(f"   - {self.config['userscripts']['media_info_script']}")
        
        print()
        print("3. 配置 PowerShell 执行策略:")
        print("   Set-ExecutionPolicy RemoteSigned")
        
        if self.config['optional_features']['auto_start_stop_server']:
            print()
            print("4. 配置 Jellyfin 服务:")
            print("   - 在 services.msc 中将 Jellyfin 设置为手动启动")
            print("   - 导入任务计划: JellyfinUAC.xml")
        
        print()
        print("5. 测试配置:")
        print(f"   运行: {self.script_dir / 'Jellyfin.bat'}")
        
        print()
        print("📖 详细说明请参考: README_CN.md")
        print("🐛 问题反馈: https://github.com/Damocles-fr/PPJF/")
    
    def run(self):
        """运行配置程序"""
        self.print_banner()
        
        # 检查是否为管理员权限
        try:
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                print("⚠️  建议以管理员权限运行此脚本以确保所有操作正常执行")
                print()
        except:
            pass
        
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
        self.update_batch_file()
        self.update_powershell_script()
        self.update_userscripts()
        self.update_task_scheduler_xml()
        self.update_task_scheduler_xml()
        
        # 应用注册表设置
        if input("应用 PotPlayer 注册表设置? (y/n) [默认: y]: ").lower() != 'n':
            self.apply_registry_settings()
        
        # 显示后续步骤
        self.show_next_steps()
        
        return True

def main():
    """主函数"""
    try:
        configurator = PPJFConfigurator()
        success = configurator.run()
        
        if success:
            print()
            print("✅ 配置完成!")
            input("按回车键退出...")
        else:
            print("❌ 配置失败!")
            input("按回车键退出...")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print()
        print("❌ 用户取消操作")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        input("按回车键退出...")
        sys.exit(1)

if __name__ == "__main__":
    main()
