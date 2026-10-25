# 启动 Django 后端（waitress 生产级 WSGI，端口 8000）
$ErrorActionPreference = 'Stop'
$root = 'D:\ecommerce\backend'
$serve = "$root\.venv\Scripts\waitress-serve.exe"
if (-not (Test-Path -LiteralPath $serve)) { throw "未找到虚拟环境，请先执行 scripts\setup_backend.ps1" }

# waitress-serve.exe 是独立进程名（非 python），需一并识别
$exist = Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.ProcessName -in @('python', 'waitress-serve') -and $_.Path -like '*ecommerce*' }
if ($exist) { Write-Host "后端已在运行 PID=$($exist.Id)"; exit 0 }

$logs = "$root\logs"
if (-not (Test-Path -LiteralPath $logs)) { New-Item -ItemType Directory -Force -Path $logs | Out-Null }
$outLog = "$logs\backend.log"
$errLog = "$logs\backend.err.log"
# stdout/stderr 必须分开文件重定向，同一文件会导致 Start-Process 报错
$p = Start-Process -FilePath $serve -ArgumentList '--listen=127.0.0.1:8000', 'config.wsgi:application' `
    -WorkingDirectory $root -WindowStyle Hidden `
    -RedirectStandardOutput $outLog -RedirectStandardError $errLog -PassThru
Start-Sleep -Seconds 3
$c = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
if ($c) {
    Write-Host "后端已启动 PID=$($p.Id) 端口 8000"
} else {
    Write-Host "后端启动异常，日志见 $errLog"
    if (Test-Path -LiteralPath $errLog) { Get-Content -LiteralPath $errLog -Tail 20 }
    exit 1
}
