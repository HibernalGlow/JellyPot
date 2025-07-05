# PPJF - Jellyfin 与 PotPlayer 整合指南

## 项目简介

本教程说明如何在 Windows 上设置 Jellyfin 服务器，实现以下功能：

- 从 Jellyfin 网页界面直接在 PotPlayer 中播放媒体文件
- 可选：从 Jellyfin 媒体信息面板一键链接到对应的本地文件夹
- 可选：启动网页界面时自动启动 Jellyfin 服务器，关闭时自动停止
- 额外功能：选择文本后一键在 IMDB、YouTube 或其他网站搜索

---

## 重要说明

- 未在 Chrome 上测试 - 推荐使用 LibreWolf，设置更简单
- 您可以在同一台电脑上安装多个 Firefox/LibreWolf/Nightly/任何分支版本。强烈建议单独安装 LibreWolf，与主浏览器分开
- 这样可以让 Jellyfin 直接在全屏模式下启动和/或隐藏浏览器菜单栏，同时启用独立配置，如 120% 默认缩放、不同的 Firefox 扩展等
- 这也允许使用可选功能，在启动网页界面时自动启动 Jellyfin 服务器，关闭窗口后停止服务器

---

## 安全提醒

- 对于可选的本地文件夹链接功能，您需要安装"native-app-setup.exe"和 Firefox 扩展"Local Filesystem Links"（作者：austrALIENsun、AWolf）
- [GitHub 仓库](https://github.com/feinstaub/webextension_local_filesystem_links)
- 如果您有安全顾虑，可以选择不安装此功能
- 我与此扩展或其创建者无任何关联
- 使用单独的 LibreWolf/Firefox 安装以降低风险

---

## 🚀 一键配置和安装（新功能！）

### 快速开始（推荐）

我们提供了一个自动配置工具，可以一键设置所有路径和配置：

1. 解压 PPJF.zip 到 `C:\ProgramData\`
2. 双击运行 `start.bat` 进行自动配置
3. 按照交互式向导输入您的路径设置，或使用默认配置
4. 配置完成后即可开始使用！

### 手动 Python 配置
如果您熟悉 Python，也可以直接运行：
1. 首次配置：`python setup.py`
2. 日常管理：`python run.py`

### 配置工具功能
- 🔍 自动检测已安装软件的路径
- ⚙️ 交互式配置所有设置参数
- 📝 自动更新所有脚本和配置文件
- 🔧 自动应用必要的注册表设置
- 🎯 创建统一的 JSON 配置文件

**现在所有路径和设置都通过 `config.json` 统一管理！**

---

## 详细安装步骤

### 0. 下载 PPJF.zip

从以下地址下载 PPJF.zip：
[https://github.com/Damocles-fr/PPJF/releases/tag/v1.0](https://github.com/Damocles-fr/PPJF/releases/tag/v1.0)

### 1. 放置必需文件

- 解压并将 PotPlayerJellyfin 文件夹移动到：
  ```
  C:\ProgramData\
  ```
- 如果您放在其他位置，请适配所有路径相关的配置

您应该有 `C:\ProgramData\PotPlayerJellyfin\` 文件夹，包含所有必需文件。

### 2. 安装 PotPlayer

- 如果已安装则无需重新安装
- 默认路径：`C:\Program Files\DAUM\PotPlayer`

### 3. 安装 LibreWolf（轻量化和隐私优化的 Firefox）

- 安装 **LibreWolf**（或任何支持 **ViolentMonkey/TamperMonkey** 扩展的分支）
- 下载地址：https://librewolf.net/installation/windows/
- 默认路径：`C:\Program Files\LibreWolf`
- 如果您想使用当前浏览器或其他浏览器，请注意步骤 10
- Local Filesystem Links 扩展存在轻微安全缺陷，建议不要在主浏览器中使用

### 4. 安装 ViolentMonkey 和脚本

- 在 LibreWolf 中，安装 ViolentMonkey 扩展
- 扩展地址：https://addons.mozilla.org/fr/firefox/addon/violentmonkey/
- LibreWolf → 设置 → 扩展 → ViolentMonkey → 点击三个点 → 点击选项
- 进入已安装的脚本
- 点击 +，然后点击新建
- 编辑器窗口将打开，显示脚本的默认元数据。删除所有默认代码行，但不要关闭窗口
- 转到 `C:\ProgramData\PotPlayerJellyfin\`
- 用记事本打开 `OpenWithPotplayerUserscript.js` 进行编辑，全选，复制
- 粘贴到您在 LibreWolf 中保持打开的 ViolentMonkey 编辑器页面
- 点击右上角的保存并退出

- 可选：如果您想要在 Jellyfin 媒体信息中显示本地文件链接
  - 在 ViolentMonkey 中执行相同操作，+，新建，删除所有行，但从 `OpenMediaInfoPathScriptmonkey.js` 文件复制/粘贴，保存并退出

### 5. 启用 PowerShell 脚本执行（Windows）

- 在 Windows 11 中，转到：设置 → 开发者 → PowerShell → 允许未签名脚本
- 或者如果找不到该选项：
  - 在开始菜单中搜索 `PowerShell`，右键点击，选择**以管理员身份运行**
  - 输入以下命令并按回车：
    ```
    Set-ExecutionPolicy RemoteSigned
    ```
  - 或者：
    ```
    Set-ExecutionPolicy RemoteSigned -Force
    ```

### 6. 应用 PotPlayer 注册表设置

- 运行 `PotPlayerMini64.reg` 并确认更改

### 7. 可选：在浏览器中保留用户登录和设置

- 让浏览器记住您的会话设置和密码
- 在 LibreWolf 中，转到设置，然后在左侧面板选择隐私与安全
- Cookie 和网站数据，点击管理例外
- 在新框中，添加 `http://localhost:8096/`（默认）或您的 Jellyfin 服务器 URL
- 保存更改
- 现在转到左侧面板的 LibreWolf
- 取消选中 ResistFingerprinting

### 8. 可选：调整 LibreWolf 全屏设置

- 仅当您想在全屏模式下使用 Jellyfin 并仍能看到 Windows 任务栏时
- 在 LibreWolf 中
- 在地址栏输入 `about:config`，如有询问请同意
- 在新页面中，搜索并输入：`full-screen-api.ignore-widgets`
- 应该显示为 false
- 双击使其变为 true
  ```
  full-screen-api.ignore-widgets true
  ```

### 9. 可选：启动时自动启用全屏

- 安装 **Auto Fullscreen** 扩展（作者：*tazeat*）
- 扩展地址：https://addons.mozilla.org/en-US/firefox/addon/autofullscreen/

### 10. 可选：如果您不使用 Jellyfin、LibreWolf 和 PotPlayer 的默认路径和 URL

- 编辑 `Jellyfin.bat`、`OpenMediaInfoPathScriptmonkey.js` 和 `OpenWithPotplayerUserscript.js`
- 这些文件设置为 LibreWolf 默认路径和 Jellyfin 服务器默认 URL：
  - `http://localhost:8096`
  - LibreWolf 路径：`C:\Program Files\LibreWolf\librewolf.exe`
  - PotPlayer 路径：`C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe`
- 如果您使用默认设置，请跳至步骤 11
- 如果不是，请编辑文件

**或者使用我们的配置工具自动设置这些路径！**

### 11. 可选：媒体信息链接到本地文件夹

- 在 LibreWolf 中，安装 **Local Filesystem Links** 扩展：
  - [Firefox 扩展页面](https://addons.mozilla.org/fr/firefox/addon/local-filesystem-links/)
  - 或者 [GitHub 仓库](https://github.com/feinstaub/webextension_local_filesystem_links)
- 如果在询问时未完成，请安装 `native-app-setup.exe`（用于本地文件资源管理器链接）
- 下载地址：https://github.com/AWolf81/webextension_local_filesystem_links-native-host-binaries/raw/master/win32/native-app-setup.exe
- 在设置页面转到扩展设置，然后选择 Local Filesystem Links，选项
- 取消选中第一个框，如果您也想在文件夹路径旁边显示文件夹图标，请选中第二个框
- 选中"显示链接（打开包含文件夹）"

### 12. 可选：仅当您希望 Jellyfin 服务器仅在您使用时运行

- 将 Jellyfin 服务器安装为服务
- 在安装过程中选择**"安装为服务"**
- 使用默认路径

如果与您已保存的 Jellyfin 设置不兼容，可以通过删除 `C:\ProgramData\Jellyfin\Server\config` 中的文件（如 network.xml 和可能的其他文件）来重置某些设置。
⚠️ 这将重置您的服务器设置 ⚠️

### 13. 配置 Jellyfin 服务仅在 LibreWolf 启动时启动，关闭时停止

- 搜索并打开**服务**（在 Windows 开始菜单中）。或按 `Win + R`，输入 `services.msc`，然后按回车
- 向下滚动找到列表中的 **Jellyfin**
- 右键点击并选择**属性**
- 在**启动类型**下拉菜单中，选择**手动**（这样它只会通过快捷方式启动，而不会在系统启动时启动）
- 点击**应用**，然后点击**确定**

### 14. 配置 Windows 管理员提示跳过

每次通过快捷方式启动 Jellyfin 服务时，都会出现管理员窗口，要阻止这种情况：
- 转到 `C:\ProgramData\PotPlayerJellyfin`
- 右键点击快捷方式"Jellyfin"并选择**属性**
- 点击**高级...**并选中**以管理员身份运行**
- 应用并保存更改

### 15. 通过设置 Windows 任务计划程序跳过 Windows 管理员提示

- 运行 Windows 任务计划程序
- 在右侧面板，点击导入任务
- 在窗口中，选择位于 `C:\ProgramData\PotPlayerJellyfin\` 的 XML 文件 `JellyfinUAC.xml`
- 在新窗口中，点击用户或组，然后找到您的用户名，您可以在框中输入您的 Windows 用户名，然后点击验证，然后确定
- 您可以自定义其他设置，但这样应该就能工作
- 保存并退出

### 16. 创建快捷方式

- 转到 `C:\ProgramData\PotPlayerJellyfin`
- `JellyfinUAC` 是主快捷方式，**请勿移动**
- 右键点击它，复制，然后转到 `C:\ProgramData\Microsoft\Windows\Start Menu\Programs`
- 在那里，右键点击并"粘贴为快捷方式"
- 现在，您可以右键点击它并发送到桌面（创建快捷方式）
- 或右键点击它，复制，然后在任何您想要的地方"粘贴为快捷方式"，重命名并更改图标
- 如果您想让它看起来像一个应用程序，没有任何标签和 Firefox 栏，请编辑 .bat 文件并在第 16 行的 -url 旁边添加 -kiosk
  - -kiosk 不适用于本地文件链接，并阻止使用新标签页或第 18 项额外功能，请改用步骤 8 和 9

### 17. 可选：自定义快捷方式（不启动/停止 Jellyfin 服务器）

- 在桌面上右键点击，新建快捷方式，输入：
  ```
  "C:\Program Files\LibreWolf\librewolf.exe" http://localhost:8096/web/index.html#/home.html
  ```
- 或者如果您想让它看起来像一个应用程序，没有任何标签和 Firefox 栏，添加 -kiosk：
  ```
  "C:\Program Files\LibreWolf\librewolf.exe" -kiosk http://localhost:8096/web/index.html#/home.html
  ```
  - -kiosk 不适用于本地文件链接，并阻止使用新标签页或第 18 项额外功能，请改用步骤 8 和 9
- 命名为 Jellyfin，在新图标快捷方式上右键点击，更改图标，浏览...，`C:\Program Files\Jellyfin\Server`，选择图标
- 要在 Windows 任务栏中显示 Jellyfin 图标而不是 LibreWolf，转到 `C:\Program Files\LibreWolf` 并对 LibreWolf.exe 执行相同操作
- 或者您可以只是收藏 Jellyfin 或将其设为 LibreWolf 的起始页

### 18. 可选：额外功能

- **Swift Selection Search**（作者：Daniel Lobo）
- 扩展地址：https://addons.mozilla.org/fr/firefox/addon/swift-selection-search/
- 使用此扩展，当您在浏览器中选择文本（如电影标题或演员姓名）时，会出现一个带有网站徽标的框
- 点击它会自动转到新标签页并在网站上搜索选定的文本
- 您可以添加 IMDB、YouTube、Wikipedia、Steam、Google Maps、翻译器、许多合法网站，或在扩展设置中自定义任何您想要的网站搜索...

### 19. 可选：C:\ProgramData\PotPlayerJellyfin 中的文件

- `potplayer.ps1`：请勿删除。主脚本
- `potplayer.reg`：请勿删除。您可能需要运行它，特别是在 PotPlayer 更新后
- `README.md`：英文说明文档
- `README_CN.md`：您正在阅读的中文说明文档
- `Jellyfin.bat`、`Jellyfin`、`JellyfinUAC`、`JellyfinUAC.xml`：仅用于服务器启动/停止和快捷方式
- `OpenMediaInfoPathScriptmonkey.js`：备份文件，在浏览器的 ViolentMonkey 中，仅用于本地链接
- `OpenWithPotplayerUserscript.js`：备份文件，在浏览器的 ViolentMonkey 中
- `config.json`：配置文件，包含所有路径设置
- `setup.py`：自动配置工具

## 重要提示

- 有时如果停止工作（可能由于 **PotPlayer 更新**或某些特定设置更改），只需**重新运行** `PotPlayerMini64.reg`
- 应该没问题，但如果发生得太频繁，您可以添加一行或创建 .bat 文件在每次或系统启动时运行 PotPlayerMini64.reg
- 未在 NAS 或网络驱动器上测试，如果有效请告诉我，如果无效，可能需要调整 .ps1 文件
- [启动和停止 Jellyfin 服务器] 如果您在关闭浏览器之前关闭 .bat（黑色窗口），Jellyfin 服务器将继续在后台运行
- [启动和停止 Jellyfin 服务器] 每次 Jellyfin 服务器更新后，转到 Windows `services.msc` **Jellyfin** **启动类型** **手动**

## 需要帮助？

- 访问：[Jellyfin 论坛主题](https://forum.jellyfin.org/t-guide-jellyfin-with-potplayer) 或**私信我** https://forum.jellyfin.org/u-damocles
- GitHub: https://github.com/Damocles-fr/PPJF/

---

## 自动配置工具说明

我们提供了一个 Python 配置工具，可以自动设置所有路径和配置。运行 `python setup.py` 后，工具将：

1. 扫描您的系统以查找已安装的软件
2. 提供默认路径建议
3. 允许您自定义任何路径
4. 自动更新所有配置文件
5. 生成正确的快捷方式和脚本

配置保存在 `config.json` 文件中，您可以随时重新运行工具来更新设置。
