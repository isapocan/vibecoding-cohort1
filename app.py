from flask import Flask, request, jsonify, send_from_directory
from llm import call_llm

app = Flask(__name__, static_folder="frontend")


@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    system_instructions = data.get("system_instructions", "")
    user_prompt = data.get("user_prompt", "")
    model = data.get("model", "gpt-4.1-mini")

    result = call_llm(system_instructions, user_prompt, model)
    return jsonify({"response": result})


if __name__ == "__main__":
    app.run(debug=True)
