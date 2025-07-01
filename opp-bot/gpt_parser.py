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
    #ROLE
    You are an expert browser automation agent.

    #GOAL
    Translate the user's natural language task into a strict sequence of Playwright-compatible JSON actions.

    #SUPPORTED_ACTIONS
    - { "action": "goto", "url": "..." }
    - { "action": "type", "selector": "...", "text": "..." }
    - { "action": "click", "selector": "..." }
    - { "action": "press", "selector": "...", "key": "Enter" }
    - { "action": "waitForSelector", "selector": "..." }
    - { "action": "screenshot", "selector": "...", "path": "filename.png" }
    - { "action": "extractText", "selector": "..." }
    - { "action": "scrollIntoView", "selector": "..." }

    #CONSTRAINTS
    - Always use selectors from the page (IDs > placeholders > class names).
    - Include a `waitForSelector` before interacting with any dynamic element.
    - Use `press` instead of clicking a search button.
    - Return only raw, valid JSON — no markdown, no extra text.

    #OUTPUT
    Return a single JSON array containing the ordered steps.
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

def system_instructions(prompt, page_url, page_title, dom_summary, step_history):
    system_prompt =  f"""
    #ROLE
    You are a strategic browser automation planner.

    #TASK
    {prompt}

    #PAGE
    - URL: {page_url}
    - Title: {page_title}

    #DOM
    {json.dumps(dom_summary, indent=2)}

    #STEP_HISTORY
    {json.dumps(step_history, indent=2)}

    #GOAL
    Infer the best next high-confidence subgoal to achieve the user's intent.

    #INSTRUCTIONS
    - Do not return JSON here.
    - Think clearly and break down next steps in natural language (e.g., “Click X”, “Type Y”).
    - Be aware of prior steps to avoid duplication.
    - If the goal is likely complete, suggest fallback behavior (e.g. screenshot).

    #OUTPUT
    Respond with a natural-language step plan only.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            { "role": "system", "content": system_prompt }
        ],
        temperature=0.2
    )
    print("SYSTEM INSTRUCTIONS:", response.choices[0].message.content.strip())
    return response.choices[0].message.content.strip()



def browser_instructions_from_context(clarified_plan, prompt, page_url, page_title, dom_summary, step_history):
    json_generation_prompt = f"""
    #ROLE
    You are a browser automation executor.

    #GOAL
    Translate the strategist's step instructions into a JSON array of Playwright-compatible actions.

    #TASK
    "{prompt}"

    #PAGE
    URL: {page_url}
    Title: {page_title}

    #DOM
    {json.dumps(dom_summary, indent=2)}

    #STEP_HISTORY
    {json.dumps(step_history, indent=2)}

    #CLARIFIED_INSTRUCTIONS
    "{clarified_plan}"

    #SUPPORTED_ACTIONS
    - {{ "action": "goto", "url": "..." }}
    - {{ "action": "type", "selector": "...", "text": "..." }}
    - {{ "action": "click", "selector": "..." }}
    - {{ "action": "press", "selector": "...", "key": "Enter" }}
    - {{ "action": "waitForSelector", "selector": "..." }}
    - {{ "action": "screenshot", "selector": "...", "path": "filename.png" }}
    - {{ "action": "extractText", "selector": "..." }}
    - {{ "action": "scrollIntoView", "selector": "..." }}

    #CONSTRAINTS
    - Use selectors strictly from the DOM section.
    - Do not repeat already executed steps.
    - Prefer ID > placeholder > name > class.
    - Always include waitForSelector before interaction.
    - Output only valid raw JSON — no markdown or comments.

    #OUTPUT
    [
    {{ "action": "...", ... }},
    ...
    ]
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            { "role": "system", "content": json_generation_prompt }
        ],
        temperature=0.2,
    )

    generated = response.choices[0].message.content.strip()
    print("new Generated JSON Plan:\n", generated)
    return generated