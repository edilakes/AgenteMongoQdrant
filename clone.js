const https = require('https');
const crypto = require('crypto');
process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

const API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzOWJhZTNkZC0wYTc3LTRiYmUtYjZjOS03NDcyZDkxOGUyOWIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzc1MTMyOTM1fQ.lhcDV-j9Eu0vyoNcwPbYu574BeUq4amrzGVaZbeQm9k";
const URL = "https://194.61.28.46/api/v1/workflows/2UbTx5cZZl9MGl9V";
const HEADERS = { "X-N8N-API-KEY": API_KEY, "Content-Type": "application/json" };

fetch(URL, { headers: HEADERS }).then(r => r.json()).then(async wf => {
    
    // Modify for Webhook
    for (let i = 0; i < wf.nodes.length; i++) {
        if (wf.nodes[i].type === "@n8n/n8n-nodes-langchain.chatTrigger") {
            wf.nodes[i] = {
                "id": crypto.randomUUID(),
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
            };
        }
        if (wf.nodes[i].type === "@n8n/n8n-nodes-langchain.agent") {
            wf.nodes[i].parameters.text = "={{ $json.body.query }}";
        }
    }
    
    if (wf.connections["When chat message received"]) {
        wf.connections["Webhook Trigger"] = wf.connections["When chat message received"];
        delete wf.connections["When chat message received"];
    }

    const newWf = {
        name: "Agente Pure Context (Nativo) - Webhook Test",
        nodes: wf.nodes,
        connections: wf.connections,
        settings: wf.settings
    };

    const res = await fetch("https://194.61.28.46/api/v1/workflows", {
        method: "POST",
        headers: HEADERS,
        body: JSON.stringify(newWf)
    });
    
    const text = await res.text();
    console.log("Status:", res.status);
    console.log("Response:", text);
}).catch(console.error);
