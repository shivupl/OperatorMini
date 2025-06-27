import requests

response = requests.post("http://localhost:5000/automate", json={
    "prompt": "Go to Wikipedia, search for 'dog', click the first result"
})

print(response.json())