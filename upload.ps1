$body = @{
    localPath = "C:\Users\成都工业学院\.qclaw\workspace\成都工业职业技术学院国际化发展十五五规划.md"
    conflictStrategy = "ask"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:21400/proxy/qclaw-cos/upload" -Method POST -ContentType "application/json" -Body $body
