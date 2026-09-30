$body = @{
    question = "What is this video about?"
    transcript = "Test video"
} | ConvertTo-Json

Invoke-RestMethod -Uri 'http://localhost:8000/ask-ai' -Method POST -ContentType 'application/json' -Body $body
