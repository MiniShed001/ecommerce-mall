# 停止全部服务并释放端口（Nginx -> 后端 -> Redis）
Write-Host '== 停止全部服务 =='
$nginx = 'D:\ecommerce\tools\nginx\nginx.exe'
$pidFile = 'D:\ecommerce\tools\nginx\logs\nginx.pid'
if (Test-Path -LiteralPath $pidFile) {
    & $nginx -p 'D:/ecommerce/tools/nginx/' -c 'D:/ecommerce/deploy/nginx/nginx.conf' -s stop
    Start-Sleep -Seconds 1
}
# pid 文件可能过期（master 换过），兜底按端口/进程名强制停止
if (Get-NetTCPConnection -LocalPort 8080 -State Listen -ErrorAction SilentlyContinue) {
    Get-Process -Name nginx -ErrorAction SilentlyContinue | Stop-Process -Force
    Write-Host 'Nginx 已停止（兜底强制停止）'
} else {
    Write-Host 'Nginx 已停止'
}
Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.ProcessName -in @('python', 'waitress-serve') -and $_.Path -like '*ecommerce*' } | Stop-Process -Force -ErrorAction SilentlyContinue
Write-Host '后端已停止'
$rcli = 'D:\ecommerce\tools\redis\redis-cli.exe'
if (Test-Path -LiteralPath $rcli) { & $rcli -p 6379 shutdown nosave 2>$null }
Start-Sleep -Seconds 1
Get-Process -Name redis-server -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Write-Host 'Redis 已停止'
Start-Sleep -Seconds 1
foreach ($port in 8080, 8000, 6379) {
    $line = netstat -ano | Select-String ":$port\s.*LISTENING" | Select-Object -First 1
    if ($line) { Write-Host "端口 $port 仍被占用：$line" } else { Write-Host "端口 $port 已释放" }
}
