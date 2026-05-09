from flask import Flask, Response, request, send_from_directory, stream_with_context
from llm import stream_llm

app = Flask(__name__, static_folder="frontend")

ALLOWED_MODELS = {"gpt-4.1-mini", "gpt-4.1", "gpt-4o", "gpt-4o-mini"}


@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    system_instructions = data.get("system_instructions", "")
    user_prompt = data.get("user_prompt", "").strip()
    model = data.get("model", "gpt-4.1-mini")

    if not user_prompt:
        return {"error": "user_prompt bos olamaz"}, 400

    if model not in ALLOWED_MODELS:
        return {"error": "Gecersiz model"}, 400

    def generate():
        try:
            yield from stream_llm(system_instructions, user_prompt, model)
        except Exception:
            yield "\n[HATA: Model yaniti alinirken bir sorun olustu.]"

    return Response(
        stream_with_context(generate()),
        mimetype="text/plain",
    )


if __name__ == "__main__":
    app.run(debug=True)
