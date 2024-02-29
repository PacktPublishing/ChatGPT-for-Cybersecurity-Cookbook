import requests 

url = "http://localhost:8001/v1/chat/completions" 

headers = {"Content-Type": "application/json"} 

data = { "messages": [
    {
        "content": "Analyze the Incident Response Plan for key strategies"
    }
], 
    "use_context": True, 
    "context_filter": None, 
    "include_sources": False, 
    "stream": False 
} 

response = requests.post(url, headers=headers, json=data) 
result = response.json() 
print(result) 
