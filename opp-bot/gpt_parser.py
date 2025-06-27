import os
import openai
from dotenv import load_dotenv

load_dotenv()
print("hi")
openai.api_key = os.getenv("OPENAI_API_KEY")

print("Loaded API Key:", os.getenv("OPENAI_API_KEY"))



def brower_instructions(prompt):
    my_prompt = """
    You are an expert in browser automation. Convert the user's request into a JSON list of actions.
    Each action should follow this format:
    [
      { "action": "goto", "url": "..." },
      { "action": "type", "selector": "...", "text": "..." },
      { "action": "click", "selector": "..." },
      ...
    ]
    Only return valid JSON. Do not include markdown or explanations.
    """
    response = openai.ChatCompletion.create(
        model = "gpt-4o",
        messages = [
            { "role": "system", "content": my_prompt },
            { "role": "user", "content": prompt }
        ],
        temperature=0.2,
        #response_format={"type": "json_object"},
    )

    return response.choices[0].message.content






