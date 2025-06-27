import requests

response = requests.post("http://localhost:5000/automate", json={
    "prompt": "Go to Amazon and find the cheapest wireless mouse under $20."
})

print(response.json())