 import requests


url = "http://localhost:1234/api/v1/chat"
model = "google/gemma-3-4b"
prompt = "explain the ai convert this into hindi "
payload = {
    "model" : model,
    "input" : prompt
}
response = requests.post(url,json = payload)  

print(response)
print(response.json())