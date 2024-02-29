curl http://localhost:1234/v1/chat/completions \ 
-H "Content-Type: application/json" \ 
-d '{ "messages": [ { "role": "system", "content": "You are a cybersecurity expert with 25 years of experience and acting as my cybersecurity advisor." }, { "role": "user", "content": "Generate an IR Plan template." } ], "temperature": 0.7, "max_tokens": -1, "stream": false }' 
