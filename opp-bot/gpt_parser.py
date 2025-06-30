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
    You are a browser automation expert. Convert the user's high-level request into a raw JSON array of Playwright-compatible actions.

    Supported actions (strict format):
    - { "action": "goto", "url": "..." }
    - { "action": "type", "selector": "...", "text": "..." }
    - { "action": "click", "selector": "..." }
    - { "action": "press", "selector": "...", "key": "Enter" }
    - { "action": "waitForSelector", "selector": "..." }
    - { "action": "screenshot", "selector": "...", "path": "filename.png" }
    - { "action": "extractText", "selector": "..." }
    - { "action": "scrollIntoView", "selector": "..." }

    Rules:
    - Always include a waitForSelector before interacting with dynamic elements.
    - Use press on the input field instead of clicking a search button.
    - Use clear, specific selectors (IDs > placeholders > classes).
    - Return only valid JSON — no explanation, markdown, or surrounding text.
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
    You are a browser automation expert. Continue a Playwright automation task by returning the next valid JSON step(s).

    User goal:
    "{og_prompt}"

    Current page:
    - URL: {page_url}
    - Title: {page_title}

    Visible DOM elements (verified and pre-sanitized):
    {json.dumps(dom_summary, indent=2)}

    Already Executed steps (DO NOT repeat unless retrying a failed action):
    {json.dumps(step_history, indent=2)}

    Instructions:
    - Return the next JSON step(s) using only selectors from the DOM above.
    - Do not fabricate or modify selectors — use only those listed.
    - Always include waitForSelector before interacting.
    - Prefer selectors in this order: IDs > placeholders > classes/names.
    - If no further steps are needed or none are valid, return an empty list or an extractText fallback.
    - If the current page title already matches the user's target (e.g. "Alan Turing - Wikipedia"), then assume the goal is complete — do not repeat clicks.
    - Only output a raw JSON array. Do NOT include ```json or any formatting. Just return the JSON itself, nothing else.

    Supported actions (strict format):
    - {{ "action": "goto", "url": "..." }}
    - {{ "action": "type", "selector": "...", "text": "..." }}
    - {{ "action": "click", "selector": "..." }}
    - {{ "action": "press", "selector": "...", "key": "Enter" }}
    - {{ "action": "waitForSelector", "selector": "..." }}
    - {{ "action": "screenshot", "selector": "...", "path": "filename.png" }}
    - {{ "action": "extractText", "selector": "..." }}
    - {{ "action": "scrollIntoView", "selector": "..." }}

    Format:
    Return a strict RAW JSON array (no markdown, no explanation).
    """


    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            { "role": "system", "content": context_prompt }
        ],
        temperature=0.2,
    )

    followup = response.choices[0].message.content
    print("GPT CONTINUATION:", followup)
    return followup


def clarify_prompt(raw_prompt):
    system_instruction = """
    You are a task simplifier. Rewrite vague or natural user commands into direct, specific, and robotic browser instructions.

    Output requirements:
    - Be concise and clear.
    - Break complex tasks into sequential sub-actions.
    - Include target websites if not mentioned (infer sensibly).
    - Use specific phrases like “Go to”, “Search for”, “Click on”, “Open” etc.
    - Preserve intent and all original details, but remove ambiguity.

    Examples:
    - "Look up the weather in NYC" → "Go to google.com, search 'NYC weather today', and read the forecast."
    - "Find AI news on Bing" → "Go to bing.com, search 'latest AI breakthroughs', and click on the first article."
    - "Search for apartments in SF" → "Go to apartments.com, search 'apartments in San Francisco', and open the first listing."
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            { "role": "system", "content": system_instruction },
            { "role": "user", "content": raw_prompt }
        ],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()





