# 构建 UniApp H5 产物 -> frontend\dist\build\h5（Nginx 托管目录）
$ErrorActionPreference = 'Stop'
Push-Location 'D:\ecommerce\frontend'
npm run build:h5
"build-rc=$LASTEXITCODE"
Pop-Location
