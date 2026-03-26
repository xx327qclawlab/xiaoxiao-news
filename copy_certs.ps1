$src = "C:\Users\成都工业学院\Desktop\新建文件夹 (6)"
$dst = "C:\Users\成都工业学院\.qclaw\workspace\cert_source"

New-Item -ItemType Directory -Force -Path $dst | Out-Null

$pngFiles = Get-ChildItem -Path $src -Filter "*.png"
$jpgFiles = Get-ChildItem -Path $src -Filter "*.jpg"

Write-Host "PNG files:" $pngFiles.Count
Write-Host "JPG files:" $jpgFiles.Count

foreach ($f in $pngFiles) {
    Copy-Item $f.FullName -Destination $dst
}

foreach ($f in $jpgFiles) {
    Copy-Item $f.FullName -Destination $dst
}

Write-Host "Done copying"
