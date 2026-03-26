Add-Type -AssemblyName System.Drawing

$sourceFolder = "C:\qclaw_temp"
$output = "C:\qclaw_temp\certificates_combined.png"

$pngFiles = Get-ChildItem -Path $sourceFolder -Filter "*.png"
$jpgFiles = Get-ChildItem -Path $sourceFolder -Filter "*.jpg"
$files = @($pngFiles) + @($jpgFiles)

Write-Host "Loading" $files.Count "images..."

$images = @()
foreach ($f in $files) {
    $img = [System.Drawing.Image]::FromFile($f.FullName)
    $images += $img
}

$thumbWidth = 320
$cols = 4
$rows = [Math]::Ceiling($images.Count / $cols)
$padding = 20
$canvasWidth = ($thumbWidth + $padding) * $cols + $padding
$thumbHeight = [int]($thumbWidth * 1.4)
$canvasHeight = $thumbHeight * $rows + $padding * ($rows + 1)

$canvas = New-Object System.Drawing.Bitmap($canvasWidth, $canvasHeight)
$graphics = [System.Drawing.Graphics]::FromImage($canvas)
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
$graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$graphics.Clear([System.Drawing.Color]::White)

Write-Host "Combining images..."

for ($i = 0; $i -lt $images.Count; $i++) {
    $img = $images[$i]
    
    $col = $i % $cols
    $row = [Math]::Floor($i / $cols)
    
    $x = $padding + $col * ($thumbWidth + $padding)
    $y = $padding + $row * ($thumbHeight + $padding)
    
    $thumb = New-Object System.Drawing.Bitmap($thumbWidth, $thumbHeight)
    $gThumb = [System.Drawing.Graphics]::FromImage($thumb)
    $gThumb.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $gThumb.DrawImage($img, 0, 0, $thumbWidth, $thumbHeight)
    $gThumb.Dispose()
    
    $shadowBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(50, 0, 0, 0))
    $graphics.FillRectangle($shadowBrush, $x + 4, $y + 4, $thumbWidth, $thumbHeight)
    
    $pen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(220, 220, 220), 1)
    $graphics.DrawRectangle($pen, $x, $y, $thumbWidth, $thumbHeight)
    
    $graphics.DrawImage($thumb, $x, $y, $thumbWidth, $thumbHeight)
    $thumb.Dispose()
}

$canvas.Save($output, [System.Drawing.Imaging.ImageFormat]::Png)

foreach ($img in $images) {
    $img.Dispose()
}
$graphics.Dispose()
$canvas.Dispose()

Write-Host "Done! Saved to:" $output
