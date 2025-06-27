from flask import Flask, request, jsonify
from gpt_parser import browser_instructions
from automation import run_script

app = Flask(__name__)

@app.route("/automate", methods=["POST"])
def automate():
    prompt = request.json.get("prompt")
    try:
        json_plan = browser_instructions(prompt)
        run_script(json_plan)
        return jsonify({"status": "success", "message": json_plan})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
if __name__ == "__main__":
    app.run(port=5000, debug=True)

