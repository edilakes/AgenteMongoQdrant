import requests
import urllib3

urllib3.disable_warnings()
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzOWJhZTNkZC0wYTc3LTRiYmUtYjZjOS03NDcyZDkxOGUyOWIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzc1MTMyOTM1fQ.lhcDV-j9Eu0vyoNcwPbYu574BeUq4amrzGVaZbeQm9k"
URL = "https://194.61.28.46/api/v1/executions"
HEADERS = {"X-N8N-API-KEY": API_KEY, "Content-Type": "application/json"}

# 1. Trigger the execution
payload = {
    "workflowId": "2UbTx5cZZl9MGl9V"
}
res = requests.post(URL, headers=HEADERS, verify=False, json=payload)
print(f"Status: {res.status_code}")
print(res.text)
