import requests
import urllib3

urllib3.disable_warnings()

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzOWJhZTNkZC0wYTc3LTRiYmUtYjZjOS03NDcyZDkxOGUyOWIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzc1MTMyOTM1fQ.lhcDV-j9Eu0vyoNcwPbYu574BeUq4amrzGVaZbeQm9k"
HEADERS = {"X-N8N-API-KEY": API_KEY, "Content-Type": "application/json"}
BASE = "https://194.61.28.46"

# Strategy: strip accents from the book name before querying.
# Use a JS function that removes diacritics and builds a partial regex.
# e.g. GENESIS -> GE.NESIS -> matches GÉNESIS
strip_accents_and_regex = (
    '={{ (() => { '
    'const rawBook = $fromAI("book", "Book name in Spanish, accents optional, e.g. GENESIS or GENEIS", "string"); '
    'const chapter = $fromAI("chapter", "Chapter number as string, e.g. 3", "string"); '
    '// Build regex: replace each vowel with a pattern matching accented/unaccented version '
    'const regexStr = rawBook.toUpperCase()'
    '.replace(/A/g,"[AÀÁ]").replace(/E/g,"[EÈÉ]").replace(/I/g,"[IÌÍ]")'
    '.replace(/O/g,"[OÒÓ]").replace(/U/g,"[UÙÚ]"); '
    'return JSON.stringify({"book": {"$regex": regexStr, "$options": "i"}, "chapter": chapter}); '
    '})() }}'
)

for wf_id in ["2UbTx5cZZl9MGl9V", "vHIZBiZEwAByhfs8"]:
    wf = requests.get(f"{BASE}/api/v1/workflows/{wf_id}", headers=HEADERS, verify=False).json()

    for node in wf["nodes"]:
        if node["type"] == "n8n-nodes-base.mongoDbTool" and node["name"] == "MongoDB Biblia":
            node["parameters"]["query"] = strip_accents_and_regex
            print(f"  Fixed MongoDB Biblia in {wf_id}")

    payload = {k: wf[k] for k in ["name", "nodes", "connections", "settings"] if k in wf}
    res = requests.put(f"{BASE}/api/v1/workflows/{wf_id}", headers=HEADERS, verify=False, json=payload)
    print(f"  Updated {wf_id}: {res.status_code}")

print("\n--- Testing webhook ---")
test = requests.post(
    f"{BASE}/webhook/test-agent",
    verify=False,
    headers={"Content-Type": "application/json"},
    json={"query": "¿Cuántos versículos tiene el capítulo 3 del Génesis?", "sessionId": "test-001"},
    timeout=90
)
print(f"Status: {test.status_code}")
print(test.text[:3000])
