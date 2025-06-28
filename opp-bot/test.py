import requests

response = requests.post("http://localhost:5000/automate", json={
    "prompt": "Go to Wikipedia, search for 'Alan Turing', and open the article about him."
})

print(response.json())