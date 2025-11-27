from flask import Flask, render_template, request, redirect
import requests
import os

app = Flask(__name__)

USER_SERVICE = os.environ.get("USER_SERVICE", "http://user-service:5000")
STATS_SERVICE = os.environ.get("STATS_SERVICE", "http://stats-service:6000")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        if name and email:
            requests.post(f"{USER_SERVICE}/users", json={"name": name, "email": email})
        return redirect("/")

    # Liste des utilisateurs
    users_resp = requests.get(f"{USER_SERVICE}/users").json()
    # Statistiques
    stats_resp = requests.get(f"{STATS_SERVICE}/stats").json()
    total_users = stats_resp.get("total_users", 0)

    return render_template("index.html", users=users_resp, total_users=total_users)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
