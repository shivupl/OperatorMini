import requests

response = requests.post("http://localhost:5000/automate", json={
    # "prompt": "Go to Wikipedia, search for 'Alan Turing', and open the article about him."
    # "prompt": "Go to Amazon.sg, search for 'noise cancelling headphones', and open the first product listing."
    #"prompt": "Go to YouTube and search for beginner Python tutorials."
    # "prompt": "Look up today's weather in New York on Google."
    "prompt": "find a recent news article about the latest AI breakthroughs, use bing to find the article"
    # "prompt": "buy me a pair of noise cancelling headphones"
    # "prompt": "book me a flight from new york to london"
    # "prompt": "Check the price of the iPhone 15 Pro on BestBuy and take a screenshot of the product page."
    # "prompt": "Go to cnn.com, search for 'latest AI breakthroughs', and open the first article."

})

print(response.json())