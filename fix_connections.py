import requests
import json
import urllib3

urllib3.disable_warnings()
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzOWJhZTNkZC0wYTc3LTRiYmUtYjZjOS03NDcyZDkxOGUyOWIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzc1MTMyOTM1fQ.lhcDV-j9Eu0vyoNcwPbYu574BeUq4amrzGVaZbeQm9k"
URL = "https://194.61.28.46/api/v1/workflows/2UbTx5cZZl9MGl9V"
HEADERS = {"X-N8N-API-KEY": API_KEY, "Content-Type": "application/json"}

res = requests.get(URL, headers=HEADERS, verify=False)
wf = res.json()

# Fix strictly the nested array for connections
wf["connections"]["Gemini Embeddings"] = {
    "ai_embedding": [
        [
            {
                "node": "Qdrant Context Map",
                "type": "ai_embedding",
                "index": 0
            },
            {
                "node": "Qdrant Library",
                "type": "ai_embedding",
                "index": 0
            }
        ]
    ]
}

payload = {k: wf[k] for k in ["name", "nodes", "connections", "settings"] if k in wf}
res_put = requests.put(URL, headers=HEADERS, verify=False, json=payload)
print(res_put.status_code)
