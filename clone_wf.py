import requests
import json
import uuid
import urllib3

urllib3.disable_warnings()
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzOWJhZTNkZC0wYTc3LTRiYmUtYjZjOS03NDcyZDkxOGUyOWIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzc1MTMyOTM1fQ.lhcDV-j9Eu0vyoNcwPbYu574BeUq4amrzGVaZbeQm9k"
URL = "https://194.61.28.46/api/v1/workflows/2UbTx5cZZl9MGl9V"
HEADERS = {"X-N8N-API-KEY": API_KEY, "Content-Type": "application/json"}

try:
    res = requests.get(URL, headers=HEADERS, verify=False)
    wf = res.json()

    for i, node in enumerate(wf["nodes"]):
        if node["type"] == "@n8n/n8n-nodes-langchain.chatTrigger":
            wf["nodes"][i] = {
                "id": str(uuid.uuid4()),
                "name": "Webhook Trigger",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1.1,
                "position": [0, 0],
                "parameters": {
                    "httpMethod": "POST",
                    "path": "test-agent",
                    "responseMode": "lastNode",
                    "options": {}
                }
            }
        if node["type"] == "@n8n/n8n-nodes-langchain.agent":
            wf["nodes"][i]["parameters"]["text"] = "={{ $json.body.query }}"

    if "When chat message received" in wf["connections"]:
        wf["connections"]["Webhook Trigger"] = wf["connections"].pop("When chat message received")

    new_wf = {
        "name": "Agente Pure Context (Nativo) - Webhook Test",
        "nodes": wf["nodes"],
        "connections": wf["connections"],
        "settings": wf.get("settings", {})
    }

    res_create = requests.post("https://194.61.28.46/api/v1/workflows", headers=HEADERS, verify=False, json=new_wf)
    
    with open("wf_clone_result.txt", "w") as f:
        f.write(f"Status: {res_create.status_code}\n")
        f.write(res_create.text)
except Exception as e:
    with open("wf_clone_result.txt", "w") as f:
        f.write(f"Error: {str(e)}")
