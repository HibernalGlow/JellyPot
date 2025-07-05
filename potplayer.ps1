Add-Type -Assembly System.Web

# 从参数获取路径
$path = $args[0]
$path = $path -replace "potplayer://" , ""

# 解码 URL
$path = $path -replace "\+", "%2B"
$path = [System.Web.HttpUtility]::UrlDecode($path)

# 清理斜杠和反斜杠
$path = $path -replace "///", "\"
$path = $path -replace "\\\\", "\"
$path = $path -replace "\\", "\"
$path = $path -replace "//", "\"

# 修正所有磁盘驱动器路径
$path = $path -replace "^([A-Z]):\\", '$1:\'
$path = $path -replace "^([A-Z])/", '$1:\'
$path = $path -replace "^([A-Z]):", '$1:\'

# 替换特定的 \\?\ 路径格式
$path = $path -replace "([A-Z]):\\\\\?\\", '$1:\'
$path = $path -replace "\\\\\?\\", "\"

# 将所有剩余的斜杠规范化为反斜杠
$path = $path -replace "/", "\"

Write-Host "标准化路径: $path"
# 使用标准化路径启动 PotPlayer
& "D:\scoop\apps\potplayer\current\PotPlayerMini64.exe" $path
