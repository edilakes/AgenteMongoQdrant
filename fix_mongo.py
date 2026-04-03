import requests
import json
import urllib3

urllib3.disable_warnings()
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzOWJhZTNkZC0wYTc3LTRiYmUtYjZjOS03NDcyZDkxOGUyOWIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzc1MTMyOTM1fQ.lhcDV-j9Eu0vyoNcwPbYu574BeUq4amrzGVaZbeQm9k"
URL = "https://194.61.28.46/api/v1/workflows/2UbTx5cZZl9MGl9V"
HEADERS = {"X-N8N-API-KEY": API_KEY, "Content-Type": "application/json"}

res = requests.get(URL, headers=HEADERS, verify=False)
wf = res.json()

for node in wf.get("nodes", []):
    if node["type"] == "n8n-nodes-base.mongoDbTool":
        if node["name"] == "MongoDB Biblia":
            desc = "Un string con un objeto JSON válido para filtrar en MongoDB. DEBE incluir las comillas dobles. Ejemplo exacto: {\"book\": \"GÉNESIS\", \"chapter\": \"3\"}"
        elif node["name"] == "MongoDB Reader":
            desc = "Un string con un objeto JSON válido para filtrar en OposicionesDB. Ejemplo: {\"tema\": \"1\"}"
        elif node["name"] == "MongoDB Itheca":
            desc = "Un string con un objeto JSON válido para filtrar en itheca. Ejemplo: {\"id\": \"123\"}"
        
        node["parameters"]["query"] = f"={{{{ JSON.parse($fromAI('mongo_query_string', '{desc}')) }}}}"
        # Remove the global description parameter if it was added as a workaround earlier
        if "description" in node["parameters"]:
            del node["parameters"]["description"]

payload = {k: wf[k] for k in ["name", "nodes", "connections", "settings"] if k in wf}
res_put = requests.put(URL, headers=HEADERS, verify=False, json=payload)
print(res_put.status_code)
