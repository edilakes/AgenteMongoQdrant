import requests
import json
import urllib3

urllib3.disable_warnings()
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzOWJhZTNkZC0wYTc3LTRiYmUtYjZjOS03NDcyZDkxOGUyOWIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzc1MTMyOTM1fQ.lhcDV-j9Eu0vyoNcwPbYu574BeUq4amrzGVaZbeQm9k"
URL = "https://194.61.28.46/api/v1/workflows/2UbTx5cZZl9MGl9V"
HEADERS = {"X-N8N-API-KEY": API_KEY, "Content-Type": "application/json"}

res = requests.get(URL, headers=HEADERS, verify=False)
wf = res.json()

# Modify nodes
for node in wf.get("nodes", []):
    if node["name"] == "MongoDB Biblia":
        node["parameters"]["description"] = "Busca textos bíblicos. En el campo 'query', pasa EXACTAMENTE este JSON: {\"book\": \"GÉNESIS\", \"chapter\": \"3\"}. Nota: book debe estar todo en mayúsculas y con tildes (ej: ÉXODO, NÚMEROS). chapter y verse DEBEN ser strings, no números enteros!"
    elif node["name"] == "Qdrant Context Map":
        node["parameters"]["description"] = "Busca rutas semánticas directas. Pasa en 'query' el concepto que buscas."
    elif node["name"] == "Qdrant Library":
        node["parameters"]["description"] = "Búsqueda semántica general (RAG). Pasa en 'query' un resumen de la pregunta."

# Add Embeddings node
emb_node = {
    "id": "gemini-embeddings-id",
    "name": "Gemini Embeddings",
    "type": "@n8n/n8n-nodes-langchain.embeddingsGoogleGemini",
    "typeVersion": 1,
    "position": [480, -320],
    "parameters": {
        "modelName": "models/text-embedding-004",
        "options": {}
    },
    "credentials": {
        "googlePalmApi": {
            "id": "ODlqO5FnJjHcsGT0",
            "name": "Google Gemini(PaLM) Api account"
        }
    }
}
wf["nodes"].append(emb_node)

# Add connections for embeddings
wf["connections"]["Gemini Embeddings"] = {
    "ai_embedding": [
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
}

payload = {k: wf[k] for k in ["name", "nodes", "connections", "settings"] if k in wf}
res_put = requests.put(URL, headers=HEADERS, verify=False, json=payload)
print(res_put.status_code)
