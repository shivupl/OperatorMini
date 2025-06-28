import os
import openai
from dotenv import load_dotenv

load_dotenv()
print("hi")
openai.api_key = os.getenv("OPENAI_API_KEY")

print("Loaded API Key:", os.getenv("OPENAI_API_KEY"))



def browser_instructions(prompt):
    my_prompt = """
    You are an expert in browser automation. Convert the user's request into a JSON list of actions that can be run by a Playwright script.

    Supported actions:
    - goto: { "action": "goto", "url": "..." }
    - type: { "action": "type", "selector": "...", "text": "..." }
    - click: { "action": "click", "selector": "..." }
    - press: { "action": "press", "selector": "...", "key": "Enter" }
    - waitForSelector: { "action": "waitForSelector", "selector": "..." }
    - screenshot: { "action": "screenshot", "selector": "...", "path": "filename.png" }
    - extractText: { "action": "extractText", "selector": "..." }
    - scrollIntoView: { "action": "scrollIntoView", "selector": "..." }

    Requirements:
    - Use "press" instead of "click" to submit search bars when appropriate.
    - Use "waitForSelector" before interacting with content that may load dynamically.
    - Only return valid raw JSON — no code blocks, markdown, or explanation.
    - Use `press` on the input field itself, not on buttons
    - If the search leads directly to the page, no click is needed after
"""
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            { "role": "system", "content": my_prompt },
            { "role": "user", "content": prompt }
        ],
        temperature=0.2,
        #response_format={"type": "json_object"},
    )
    print( response.choices[0].message.content )

    return response.choices[0].message.content






