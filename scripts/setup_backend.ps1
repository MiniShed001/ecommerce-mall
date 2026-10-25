# 一键初始化后端：建虚拟环境 -> 装依赖(D盘缓存) -> 迁移 -> 初始化数据 -> 收集静态文件
$ErrorActionPreference = 'Stop'
$root = 'D:\ecommerce\backend'
$venvPy = "$root\.venv\Scripts\python.exe"

if (-not (Test-Path -LiteralPath "$root\.venv")) {
    Write-Host '== 创建虚拟环境 =='
    & 'D:\pythonDownLoad\python.exe' -m venv "$root\.venv"
}

$env:PIP_CACHE_DIR = 'D:\ecommerce\.pip-cache'

Write-Host '== 安装依赖(清华镜像, 缓存于D盘) =='
& $venvPy -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
& $venvPy -m pip install -r "$root\requirements.txt" -i https://pypi.tuna.tsinghua.edu.cn/simple
if ($LASTEXITCODE -ne 0) { throw 'pip 安装失败' }

Write-Host '== 数据库迁移 =='
& $venvPy "$root\manage.py" migrate
if ($LASTEXITCODE -ne 0) { throw 'migrate 失败' }

Write-Host '== 初始化示例数据 =='
& $venvPy "$root\manage.py" seed_data
if ($LASTEXITCODE -ne 0) { throw 'seed_data 失败' }

Write-Host '== 收集静态文件 =='
& $venvPy "$root\manage.py" collectstatic --noinput

Write-Host '后端初始化完成'
