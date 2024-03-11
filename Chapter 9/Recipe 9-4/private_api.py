import requests 

url = "http://localhost:8001/v1/chat/completions" 

headers = {"Content-Type": "application/json"} 
data = { "messages": [
    {
        "content": "Analyze the Incident Response Plan for potential gaps and weaknesses."
    }
], 
    "use_context": True, 
    "context_filter": None, 
    "include_sources": False, 
    "stream": False 
} 

response = requests.post(url, headers=headers, json=data) 
result = response.json().get('choices')[0].get('message').get('content').strip()
print(result) 
