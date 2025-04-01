import requests
def chat(query):
    url = "http://127.0.0.1:8001/api/chat-llm" 
    data = {
        "query": f"{query}",
        "user_id": "string",
        "session_id": "string"
    }
    response  = requests.post(url, json=data)
    return response.json()['answer']

