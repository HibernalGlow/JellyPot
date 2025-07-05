#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PPJF 配置更新工具
用于更新现有配置文件中的路径设置
"""

import json
import os
from pathlib import Path

def update_config_from_existing_files():
    """从现有文件中提取配置并更新 config.json"""
    script_dir = Path(__file__).parent.absolute()
    config_file = script_dir / "config.json"
    
    # 读取当前配置
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    else:
        print("❌ config.json 文件不存在，请先运行 setup.py")
        return
    
    # 从 Jellyfin.bat 中提取信息
    batch_file = script_dir / "Jellyfin.bat"
    if batch_file.exists():
        with open(batch_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取浏览器路径
        for line in content.split('\n'):
            if 'start ""' in line and '.exe' in line:
                parts = line.split('"')
                for part in parts:
                    if part.endswith('.exe'):
                        config['browser']['executable_path'] = part
                        config['browser']['process_name'] = Path(part).name.lower()
                        break
        
        # 提取 Jellyfin URL
        for line in content.split('\n'):
            if 'curl -s' in line:
                url = line.split('curl -s ')[1].split(' ')[0]
                config['jellyfin']['server_url'] = url
                break
    
    # 从 potplayer.ps1 中提取 PotPlayer 路径
    ps_file = script_dir / "potplayer.ps1"
    if ps_file.exists():
        with open(ps_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for line in content.split('\n'):
            if 'PotPlayerMini64.exe' in line and '&' in line:
                # 提取引号中的路径
                parts = line.split('"')
                for part in parts:
                    if 'PotPlayerMini64.exe' in part:
                        config['potplayer']['executable_path'] = part
                        break
    
    # 从用户脚本中提取 Jellyfin URL
    userscript_file = script_dir / "OpenWithPotplayerUserscript.js"
    if userscript_file.exists():
        with open(userscript_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for line in content.split('\n'):
            if '@match' in line and 'http' in line:
                url_part = line.split('http')[1].split('/web')[0]
                url = 'http' + url_part
                config['jellyfin']['server_url'] = url
                break
    
    # 保存更新的配置
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✅ 配置已从现有文件中更新")
    return config

if __name__ == "__main__":
    update_config_from_existing_files()
