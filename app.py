from flask import Flask, render_template, request, Response, stream_with_context, session
import os
import time

from pdf_loader import load_pdf_text
from qa_engine import split_text, answer_from_pdf_stream

app = Flask(__name__)
app.secret_key = "nebula-ai-session-key"

# ---------- LOAD PDF ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(BASE_DIR, "data", "sample.pdf")

text = load_pdf_text(PDF_PATH)
chunks = split_text(text)

# ---------- ROUTES ----------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return Response("", mimetype="text/plain")

    # 🔹 Short-term memory
    last_q = session.get("last_question", "")
    last_a = session.get("last_answer", "")

    @stream_with_context
    def generate():
        yield "🔍 Analyzing the document...\n"
        time.sleep(0.3)

        full_answer = ""

        for token in answer_from_pdf_stream(
            question=question,
            chunks=chunks,
            history=f"Previous Question: {last_q}\nPrevious Answer: {last_a}"
        ):
            full_answer += token
            yield token
            time.sleep(0.02)

        # 🔹 Save memory AFTER answer finishes
        session["last_question"] = question
        session["last_answer"] = full_answer

    return Response(
        generate(),
        mimetype="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
