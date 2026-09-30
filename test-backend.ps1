$body = @{
    question = "test"
    transcript = "test"
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri 'http://localhost:8000/ask-ai' -Method POST -ContentType 'application/json' -Body $body
    Write-Host "Status Code: $($response.StatusCode)"
    Write-Host "Response: $($response.Content)"
} catch {
    Write-Host "Error: $($_.Exception.Message)"
    if ($_.Exception.Response) {
        $statusCode = [int]$_.Exception.Response.StatusCode
        Write-Host "Status Code: $statusCode"
    }
}
