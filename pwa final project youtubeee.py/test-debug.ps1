$body = @{
    question = "test"
    transcript = "test"
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri 'http://localhost:8000/ask-ai' -Method POST -ContentType 'application/json' -Body $body
    Write-Host "Status Code: $($response.StatusCode)"
    Write-Host "Response: $($response.Content)"
} catch {
    Write-Host "Status Code: $($_.Exception.Response.StatusCode)"
    $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
    $reader.BaseStream.Position = 0
    $responseBody = $reader.ReadToEnd()
    $reader.Close()
    Write-Host "Response Body: $responseBody"
}
