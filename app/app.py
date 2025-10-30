from __future__ import annotations

from flask import Flask, redirect, render_template, request, url_for


app = Flask(__name__, template_folder="../templates")

# Simple in-memory scoreboard; resets whenever the container restarts.
SCORES = {
    "Chispa Unicornio": 0,
    "Senor Meme": 0,
    "Dona Fiesta": 0,
    "Capitan Karaoke": 0,
}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        vote = request.form.get("vote")
        if vote in SCORES:
            SCORES[vote] += 1
        return redirect(url_for("index"))

    total_votes = sum(SCORES.values())
    ranking = sorted(SCORES.items(), key=lambda item: item[1], reverse=True)
    return render_template("index.html", ranking=ranking, total_votes=total_votes)


@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(debug=True)
