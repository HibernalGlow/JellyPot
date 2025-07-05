# JellyPot 使用指南

## 项目结构

```
JellyPot/
├── src/jellypot/           # 主包
│   ├── config/             # 配置模块
│   │   ├── configurator.py    # 配置器
│   │   ├── config.json         # 配置文件
│   │   ├── PotPlayerMini64.reg # 注册表文件
│   │   └── runner.py           # 运行器
│   ├── core/               # 核心模块
│   │   ├── launcher.py         # 启动器
│   │   └── build.py            # 构建器
│   ├── scripts/            # 脚本文件
│   │   ├── potplayer.ps1       # PowerShell 脚本
│   │   ├── Jellyfin.bat        # 批处理文件
│   │   └── *.js                # 用户脚本
│   └── assets/             # 资源文件
├── pyproject.toml          # 项目配置
├── test.py                 # 测试脚本
└── install.py              # 安装脚本

## 安装和使用

### 1. 快速安装
```bash
# 使用 uv 安装（推荐）
uv sync

# 或者运行安装脚本
python install.py
```

### 2. 配置系统
```bash
# 运行配置器
uv run python -m jellypot.config.configurator

# 或者直接运行配置器的 run 方法
uv run python -c "from jellypot import PPJFConfigurator; PPJFConfigurator().run()"
```

### 3. 构建 exe 启动器
```bash
# 构建无头 exe
uv run python -m jellypot.core.build
```

### 4. 测试功能
```bash
# 运行测试
python test.py

# 测试启动器
uv run python -m jellypot.core.launcher "potplayer://d:/test.mp4"
```

## 功能模块

### 启动器 (PotPlayerLauncher)
- 自动检测 PotPlayer 路径
- 标准化媒体文件路径
- 支持 potplayer:// 协议
- 无头启动（不显示控制台）

### 配置器 (PPJFConfigurator)
- 自动检测软件安装路径
- 交互式配置向导
- 生成注册表文件
- 创建批处理启动器
- 更新 PowerShell 脚本

### 构建器 (build)
- 使用 PyInstaller 构建 exe
- 自动更新注册表文件
- 单文件输出，无依赖

## 开发和测试

### 开发环境设置
```bash
# 安装开发依赖
uv sync --extra dev

# 代码格式化
uv run black src/
uv run isort src/

# 类型检查
uv run mypy src/
```

### 项目打包
```bash
# 构建分发包
uv build

# 安装本地包
uv sync
```

## 项目优势

1. **现代化项目结构**: 使用 src 布局，清晰的模块分离
2. **uv 包管理**: 快速依赖管理和虚拟环境
3. **类型提示**: 全面的类型注解，提高代码质量
4. **模块化设计**: 各功能模块独立，易于维护和扩展
5. **无头执行**: 构建的 exe 启动器完全无窗口
6. **自动化配置**: 一键配置所有必要的文件和设置

## 故障排除

### 常见问题
1. **找不到 PotPlayer**: 检查 PotPlayer 是否已安装，或手动指定路径
2. **PowerShell 执行策略**: 运行 `Set-ExecutionPolicy RemoteSigned`
3. **注册表权限**: 以管理员身份运行注册表文件导入
4. **uv 未安装**: 访问 https://github.com/astral-sh/uv 安装 uv
