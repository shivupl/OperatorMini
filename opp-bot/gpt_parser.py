import os
import openai
import json
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
        model = "gpt-4o-mini",
        messages = [
            { "role": "system", "content": my_prompt },
            { "role": "user", "content": prompt }
        ],
        temperature=0.2,
        #response_format={"type": "json_object"},
    )
    print( response.choices[0].message.content )

    return response.choices[0].message.content


def new_instructions(og_prompt, page_url, page_title, dom_summary, step_history):
    context_prompt = f"""
    You are a browser automation expert continuing a Playwright script.

    🔹 User's original instruction:
    "{og_prompt}"

    🔹 Current page:
    - URL: {page_url}
    - Title: {page_title}

    🔹 DOM snapshot (visible elements, JSON list):
    {json.dumps(dom_summary, indent=2)}

    🔹 Previously executed steps (do NOT repeat unless necessary):
    {json.dumps(step_history, indent=2)}

    Your task:
    Determine the next JSON action(s) required to progress the original instruction. Only use selectors *exactly as they appear* in the DOM snapshot above — do not guess, invent, or alter attribute names.

    Selector priority:
    1. Use IDs (e.g., input#searchInput)
    2. Then placeholder (e.g., input[placeholder='Search'])
    3. Then class or name — only if no better alternative exists

    Supported actions:
    - goto: {{ "action": "goto", "url": "..." }}
    - type: {{ "action": "type", "selector": "...", "text": "..." }}
    - click: {{ "action": "click", "selector": "..." }}
    - press: {{ "action": "press", "selector": "...", "key": "Enter" }}
    - waitForSelector: {{ "action": "waitForSelector", "selector": "..." }}
    - screenshot: {{ "action": "screenshot", "selector": "...", "path": "filename.png" }}
    - extractText: {{ "action": "extractText", "selector": "..." }}
    - scrollIntoView: {{ "action": "scrollIntoView", "selector": "..." }}

    Requirements:
    - Return *only* raw valid JSON array — no markdown, no code blocks, no explanations
    - Do not repeat past steps unless they are required for continuation
    - Always use "waitForSelector" before interacting with dynamically loaded elements
    - Use "press" on the *input field*, not on surrounding buttons
    - If the task is complete or no action can be taken, return an extractText step or leave the result empty
    """


    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            { "role": "system", "content": context_prompt }
        ],
        temperature=0.2,
    )

    followup = response.choices[0].message.content
    print("GPT CONTINUATION:", followup)
    return followup





