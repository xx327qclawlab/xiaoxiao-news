Add-Type -AssemblyName System.Drawing

$sourceFolder = "C:\Users\成都工业学院\.qclaw\workspace\cert_source"
$output = "C:\Users\成都工业学院\.qclaw\workspace\certificates_combined.png"

$pngFiles = Get-ChildItem -LiteralPath $sourceFolder -Filter "*.png"
$jpgFiles = Get-ChildItem -LiteralPath $sourceFolder -Filter "*.jpg"
$files = @($pngFiles) + @($jpgFiles)

$images = @()
foreach ($f in $files) {
    $img = [System.Drawing.Image]::FromFile($f.FullName)
    $images += $img
}

$thumbWidth = 350
$cols = 4
$rows = [Math]::Ceiling($images.Count / $cols)
$padding = 25
$canvasWidth = ($thumbWidth + $padding) * $cols + $padding
$thumbHeight = [int]($thumbWidth * 1.4)
$canvasHeight = $thumbHeight * $rows + $padding * $rows + 150

$canvas = New-Object System.Drawing.Bitmap($canvasWidth, $canvasHeight)
$graphics = [System.Drawing.Graphics]::FromImage($canvas)
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
$graphics.Clear([System.Drawing.Color]::White)

$font = New-Object System.Drawing.Font("Arial", 40, [System.Drawing.FontStyle]::Bold)
$brush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(44, 62, 80))
$title = "International Certifications"
$titleSize = $graphics.MeasureString($title, $font)
$graphics.DrawString($title, $font, $brush, ($canvasWidth - $titleSize.Width) / 2, 25)

$font2 = New-Object System.Drawing.Font("Arial", 18)
$brush2 = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(127, 140, 155))
$subtitle = "Chengdu Institute of Technology - International Cooperation"
$subSize = $graphics.MeasureString($subtitle, $font2)
$graphics.DrawString($subtitle, $font2, $brush2, ($canvasWidth - $subSize.Width) / 2, 75)

for ($i = 0; $i -lt $images.Count; $i++) {
    $img = $images[$i]
    
    $col = $i % $cols
    $row = [Math]::Floor($i / $cols)
    
    $x = $padding + $col * ($thumbWidth + $padding)
    $y = 130 + $row * ($thumbHeight + $padding)
    
    $depthOffset = $row * 8
    $offsetX = (($i % 5) - 2) * 6
    $offsetY = (($i % 3) - 1) * 4
    
    $finalX = $x + $offsetX + $depthOffset
    $finalY = $y + $offsetY + [int]($depthOffset / 2)
    
    $thumb = New-Object System.Drawing.Bitmap($thumbWidth, $thumbHeight)
    $gThumb = [System.Drawing.Graphics]::FromImage($thumb)
    $gThumb.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $gThumb.DrawImage($img, 0, 0, $thumbWidth, $thumbHeight)
    $gThumb.Dispose()
    
    $shadowBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(60, 0, 0, 0))
    $graphics.FillRectangle($shadowBrush, $finalX + 6, $finalY + 6, $thumbWidth, $thumbHeight)
    
    $pen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(200, 200, 200), 1)
    $graphics.DrawRectangle($pen, $finalX, $finalY, $thumbWidth, $thumbHeight)
    
    $graphics.DrawImage($thumb, $finalX, $finalY, $thumbWidth, $thumbHeight)
    $thumb.Dispose()
}

$font3 = New-Object System.Drawing.Font("Arial", 14)
$brush3 = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(150, 150, 150))
$footer = "Total " + $images.Count + " International Certifications"
$footerSize = $graphics.MeasureString($footer, $font3)
$graphics.DrawString($footer, $font3, $brush3, ($canvasWidth - $footerSize.Width) / 2, $canvasHeight - 40)

$canvas.Save($output, [System.Drawing.Imaging.ImageFormat]::Png)

foreach ($img in $images) {
    $img.Dispose()
}
$graphics.Dispose()
$canvas.Dispose()

Write-Host "Done - Output: $output"
