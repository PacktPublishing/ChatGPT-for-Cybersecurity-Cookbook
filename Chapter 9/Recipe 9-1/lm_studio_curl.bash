# Linux/MacOS curl
curl http://localhost:1234/v1/chat/completions -H "Content-Type: application/json" -d '{ "messages": [ { "role": "system", "content": "You are a cybersecurity expert with 25 years of experience and acting as my cybersecurity advisor." }, { "role": "user", "content": "Generate an IR Plan template." } ], "temperature": 0.7, "max_tokens": -1, "stream": false }' | grep '"content":' | awk -F'"content": "' '{print $2}' | sed 's/"}]//'

#Windows PowerShell
$response = Invoke-WebRequest -Uri http://localhost:1234/v1/chat/completions -Method Post -ContentType "application/json" -Body '{ "messages": [ { "role": "system", "content": "You are a cybersecurity expert with 25 years of experience and acting as my cybersecurity advisor." }, { "role": "user", "content": "Generate an IR Plan template." } ], "temperature": 0.7, "max_tokens": -1, "stream": false }'; ($response.Content | ConvertFrom-Json).choices[0].message.content