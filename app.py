from flask import Flask, render_template, request
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


@app.route("/", methods=["GET", "POST"])
def index():
    response_text = None

    if request.method == "POST":
        user_input = request.form["text_input"]

        # Email Fixer prompt
        prompt = f"""You are Email Fixer. Rewrite the following draft email to be polite, clear, and concise, while keeping the meaning the same. Do not add fluff or extra details.

Email draft:
{user_input}
"""

        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role":
                    "system",
                    "content":
                    "You are a helpful assistant that rewrites draft emails clearly and politely."
                }, {
                    "role": "user",
                    "content": prompt
                }],
                max_tokens=500)

            response_text = completion.choices[0].message.content.strip()

        except Exception as e:
            response_text = f"Error: {e}"

    return render_template("index.html", response_text=response_text)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
