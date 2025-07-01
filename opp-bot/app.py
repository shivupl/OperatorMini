from flask import Flask, request, jsonify
from gpt_parser import browser_instructions, clarify_prompt
from automation import run_script
import asyncio

app = Flask(__name__)

@app.route("/automate", methods=["POST"])
def automate():
    prompt = request.json.get("prompt")
    try:
        p_instructions = clarify_prompt(prompt)
        print(p_instructions)
        json_plan = browser_instructions(p_instructions)
        asyncio.run(run_script(json_plan, p_instructions))
        return jsonify({"status": "success", "message": json_plan})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)