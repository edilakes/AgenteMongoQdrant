import requests
import json
import urllib3

urllib3.disable_warnings()

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzOWJhZTNkZC0wYTc3LTRiYmUtYjZjOS03NDcyZDkxOGUyOWIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzc1MTMyOTM1fQ.lhcDV-j9Eu0vyoNcwPbYu574BeUq4amrzGVaZbeQm9k"
HEADERS = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}
URL = "https://194.61.28.46/api/v1/workflows/2UbTx5cZZl9MGl9V"

# 1. Fetch
res = requests.get(URL, headers=HEADERS, verify=False)
wf = res.json()

# 2. Fix credentials
for node in wf.get("nodes", []):
    if "lmChatGoogleGemini" in node.get("type", ""):
        node["credentials"] = {
            "googlePalmApi": {
                "id": "ODlqO5FnJjHcsGT0",
                "name": "Google Gemini(PaLM) Api account"
            }
        }
    elif "mongoDbTool" in node.get("type", ""):
        if "credentials" in node.get("parameters", {}):
            node["credentials"] = node["parameters"].pop("credentials")
        else:
            node["credentials"] = {
                "mongoDb": {
                    "id": "tAHcWcGzNkjgWlwI",
                    "name": "MongoDB account"
                }
            }
    elif "qdrantTool" in node.get("type", ""):
        if "credentials" in node.get("parameters", {}):
            node["credentials"] = node["parameters"].pop("credentials")
        else:
            node["credentials"] = {
                "qdrantRestApi": {
                    "id": "luT3jOypuNOZXNkX",
                    "name": "Qdrant account"
                }
            }

# 3. Strip extra properties to avoid 400 Bad Request
allowed_keys = ["name", "nodes", "connections", "settings", "tags"]
payload = {k: wf[k] for k in allowed_keys if k in wf}

# 4. Update workflow
res_put = requests.put(URL, headers=HEADERS, verify=False, json=payload)
print(f"Status: {res_put.status_code}")
if res_put.status_code != 200:
    print(res_put.text)
else:
    print("Workflow updated successfully")
