#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PPJF 一键运行脚本
快速启动和配置 PPJF 系统
"""

import json
import os
import sys
import subprocess
from pathlib import Path

class PPJFLauncher:
    def __init__(self):
        self.script_dir = Path(__file__).parent.absolute()
        self.config_file = self.script_dir / "config.json"
        
    def load_config(self):
        """加载配置文件"""
        if not self.config_file.exists():
            print("❌ 配置文件不存在，请先运行 setup.py 进行配置")
            return None
        
        with open(self.config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def check_dependencies(self, config):
        """检查依赖项"""
        print("🔍 检查系统依赖项...")
        
        issues = []
        
        # 检查 PotPlayer
        if not os.path.exists(config['potplayer']['executable_path']):
            issues.append(f"PotPlayer 未找到: {config['potplayer']['executable_path']}")
        
        # 检查浏览器
        if not os.path.exists(config['browser']['executable_path']):
            issues.append(f"浏览器未找到: {config['browser']['executable_path']}")
        
        # 检查注册表文件
        reg_file = self.script_dir / config['potplayer']['reg_file']
        if not reg_file.exists():
            issues.append(f"注册表文件未找到: {reg_file}")
        
        # 检查脚本文件
        required_files = [
            "Jellyfin.bat",
            "potplayer.ps1",
            config['userscripts']['potplayer_script']
        ]
        
        for file_name in required_files:
            file_path = self.script_dir / file_name
            if not file_path.exists():
                issues.append(f"脚本文件未找到: {file_path}")
        
        if issues:
            print("❌ 发现以下问题:")
            for issue in issues:
                print(f"   {issue}")
            return False
        
        print("✅ 所有依赖项检查通过")
        return True
    
    def apply_registry(self, config):
        """应用注册表设置"""
        print("📝 应用 PotPlayer 注册表设置...")
        
        reg_file = self.script_dir / config['potplayer']['reg_file']
        
        try:
            subprocess.run(['regedit', '/s', str(reg_file)], check=True)
            print("✅ 注册表设置已应用")
            return True
        except subprocess.CalledProcessError:
            print("❌ 应用注册表设置失败")
            return False
    
    def start_jellyfin(self, config):
        """启动 Jellyfin"""
        print("🚀 启动 Jellyfin...")
        
        if config['optional_features']['auto_start_stop_server']:
            # 使用带自动启停功能的批处理文件
            batch_file = self.script_dir / "Jellyfin.bat"
            subprocess.Popen(str(batch_file), shell=True)
            print("✅ Jellyfin 已启动（自动管理模式）")
        else:
            # 直接启动浏览器
            browser_path = config['browser']['executable_path']
            jellyfin_url = f"{config['jellyfin']['server_url']}/web/index.html#/home.html"
            
            try:
                subprocess.Popen([browser_path, jellyfin_url])
                print("✅ Jellyfin 网页界面已启动")
            except Exception as e:
                print(f"❌ 启动浏览器失败: {e}")
                return False
        
        return True
    
    def show_menu(self):
        """显示菜单"""
        print()
        print("🎬 PPJF 一键运行工具")
        print("=" * 40)
        print("1. 检查并应用配置")
        print("2. 启动 Jellyfin")
        print("3. 重新配置")
        print("4. 查看状态")
        print("5. 退出")
        print()
        
        choice = input("请选择操作 (1-5): ").strip()
        return choice
    
    def show_status(self, config):
        """显示系统状态"""
        print()
        print("📊 系统状态")
        print("=" * 40)
        print(f"Jellyfin URL: {config['jellyfin']['server_url']}")
        print(f"浏览器: {config['browser']['type']} - {config['browser']['executable_path']}")
        print(f"PotPlayer: {config['potplayer']['executable_path']}")
        print(f"自动启停服务器: {'是' if config['optional_features']['auto_start_stop_server'] else '否'}")
        print(f"本地文件链接: {'是' if config['optional_features']['local_filesystem_links'] else '否'}")
        print()
        
        # 检查进程状态
        try:
            import psutil
            jellyfin_running = any('jellyfin' in p.name().lower() for p in psutil.process_iter(['name']))
            browser_running = any(config['browser']['process_name'].replace('.exe', '') in p.name().lower() 
                                for p in psutil.process_iter(['name']))
            
            print("进程状态:")
            print(f"  Jellyfin: {'🟢 运行中' if jellyfin_running else '🔴 未运行'}")
            print(f"  浏览器: {'🟢 运行中' if browser_running else '🔴 未运行'}")
        except ImportError:
            print("💡 安装 psutil 可查看进程状态: pip install psutil")
    
    def run(self):
        """运行主程序"""
        while True:
            config = self.load_config()
            if not config:
                print("请先运行 setup.py 进行初始配置")
                break
            
            choice = self.show_menu()
            
            if choice == '1':
                print("\n🔧 检查并应用配置...")
                if self.check_dependencies(config):
                    self.apply_registry(config)
                    print("✅ 配置检查完成")
                else:
                    print("❌ 请解决上述问题后重试")
                
            elif choice == '2':
                print("\n🚀 启动 Jellyfin...")
                if self.check_dependencies(config):
                    self.start_jellyfin(config)
                else:
                    print("❌ 请先解决依赖项问题")
                
            elif choice == '3':
                print("\n🛠️ 重新配置...")
                try:
                    subprocess.run([sys.executable, str(self.script_dir / "setup.py")])
                except Exception as e:
                    print(f"❌ 启动配置程序失败: {e}")
                
            elif choice == '4':
                self.show_status(config)
                
            elif choice == '5':
                print("👋 再见!")
                break
                
            else:
                print("❌ 无效选择，请重试")
            
            input("\n按回车键继续...")

def main():
    """主函数"""
    try:
        launcher = PPJFLauncher()
        launcher.run()
    except KeyboardInterrupt:
        print("\n👋 用户取消操作")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        input("按回车键退出...")

if __name__ == "__main__":
    main()
