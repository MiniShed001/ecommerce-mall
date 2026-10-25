# 启动 Redis（端口 6379，数据落盘 D:\ecommerce\tools\redis）
$ErrorActionPreference = 'Stop'
$redis = 'D:\ecommerce\tools\redis\redis-server.exe'
if (-not (Test-Path -LiteralPath $redis)) { throw "未找到 Redis：$redis" }
$proc = Get-Process -Name redis-server -ErrorAction SilentlyContinue
if ($proc) { Write-Host "Redis 已在运行 PID=$($proc.Id)"; exit 0 }
$p = Start-Process -FilePath $redis -ArgumentList '--port','6379','--bind','127.0.0.1','--dir','D:\ecommerce\tools\redis' -WindowStyle Hidden -PassThru
Start-Sleep -Seconds 1
Write-Host "Redis 已启动 PID=$($p.Id) 端口 6379"
