# 启动 Nginx（端口 8080）：托管前端 H5 + /api 反向代理到 Django
$ErrorActionPreference = 'Stop'
$nginx = 'D:\ecommerce\tools\nginx\nginx.exe'
if (-not (Test-Path -LiteralPath $nginx)) { throw "未找到 Nginx：$nginx" }
$pidFile = 'D:\ecommerce\tools\nginx\logs\nginx.pid'
if (Test-Path -LiteralPath $pidFile) {
    $old = Get-Content -LiteralPath $pidFile
    if ($old -and (Get-Process -Id $old -ErrorAction SilentlyContinue)) {
        Write-Host "Nginx 已在运行 PID=$old"; exit 0
    }
}
# 用 Start-Process 拉起 nginx（daemon 化后立即返回，避免 PowerShell 挂起）
Start-Process -FilePath $nginx -ArgumentList '-p', 'D:/ecommerce/tools/nginx/', '-c', 'D:/ecommerce/deploy/nginx/nginx.conf' -WindowStyle Hidden
Start-Sleep -Seconds 1
if (Get-NetTCPConnection -LocalPort 8080 -State Listen -ErrorAction SilentlyContinue) {
    Write-Host 'Nginx 已启动 端口 8080'
} else {
    Write-Host 'Nginx 启动失败，请查看 tools\nginx\logs\error.log'
    exit 1
}
