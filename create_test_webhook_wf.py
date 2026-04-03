import requests
import json
import urllib3

urllib3.disable_warnings()
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzOWJhZTNkZC0wYTc3LTRiYmUtYjZjOS03NDcyZDkxOGUyOWIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzc1MTMyOTM1fQ.lhcDV-j9Eu0vyoNcwPbYu574BeUq4amrzGVaZbeQm9k"
URL = "https://194.61.28.46/api/v1/workflows/2UbTx5cZZl9MGl9V"
HEADERS = {"X-N8N-API-KEY": API_KEY, "Content-Type": "application/json"}

# Fetch existing
res = requests.get(URL, headers=HEADERS, verify=False)
wf = res.json()

# Delete specific workflow metadata properties
for prop in ["id", "createdAt", "updatedAt", "versionId", "activeVersionId", "activeVersion", "shared", "authors"]:
    if prop in wf:
        del wf[prop]
        
wf["name"] = "Agente Pure Context (Nativo) - Webhook Test"

# Replace Trigger
for i, node in enumerate(wf["nodes"]):
    if node["type"] == "@n8n/n8n-nodes-langchain.chatTrigger":
        wf["nodes"][i] = {
            "id": "webhook-trigger-id",
            "name": "Testing Webhook",
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 1,
            "position": [0, 0],
            "parameters": {
                "httpMethod": "POST",
                "path": "test-agent",
                "responseMode": "lastNode",
                "options": {}
            }
        }
    if node["type"] == "@n8n/n8n-nodes-langchain.agent":
        # Configure agent to read from webhook's JSON "query"
        node["parameters"]["text"] = "={{ $json.query }}"

# Replace connections reference
if "When chat message received" in wf["connections"]:
    wf["connections"]["Testing Webhook"] = wf["connections"]["When chat message received"]
    del wf["connections"]["When chat message received"]

# Create new workflow
CREATE_URL = "https://194.61.28.46/api/v1/workflows"
res_create = requests.post(CREATE_URL, headers=HEADERS, verify=False, json=wf)
print(res_create.status_code)
print(res_create.text)
