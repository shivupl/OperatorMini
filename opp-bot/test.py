import requests

response = requests.post("http://localhost:5000/automate", json={
    "prompt": "Go to the wikipedia page for the golden retriever and scroll to the bottom of the page and wait for 10 seconds"
})

print(response.json())