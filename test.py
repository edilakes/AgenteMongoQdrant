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

# Simplify the cloned workflow payload
new_wf = {
    "name": "Agente Pure Context (Nativo) - Webhook Test",
    "nodes": wf.get("nodes", []),
    "connections": wf.get("connections", {})
}

# Replace Trigger
for i, node in enumerate(new_wf["nodes"]):
    if node["type"] == "@n8n/n8n-nodes-langchain.chatTrigger":
        new_wf["nodes"][i] = {
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
        node["parameters"]["text"] = "={{ $json.body.query }}"

# Replace connections reference
if "When chat message received" in new_wf["connections"]:
    new_wf["connections"]["Testing Webhook"] = new_wf["connections"].pop("When chat message received")

# Create new workflow
CREATE_URL = "https://194.61.28.46/api/v1/workflows"
res_create = requests.post(CREATE_URL, headers=HEADERS, verify=False, json=new_wf)
print(res_create.status_code)
print(res_create.text)
