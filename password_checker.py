from flask import Flask, render_template, request
import random
import string

app = Flask(__name__)

# Function to check password strength
def check_strength(password):
    strength = 0
    if len(password) >= 8:
        strength += 1
    if any(c.islower() for c in password):
        strength += 1
    if any(c.isupper() for c in password):
        strength += 1
    if any(c.isdigit() for c in password):
        strength += 1
    if any(c in "!@#$%^&*()-_=+[]{};:'\",.<>?/\\|" for c in password):
        strength += 1

    if strength <= 2:
        return "Weak"
    elif strength == 3:
        return "Medium"
    else:
        return "Strong"

# Function to generate a strong password
def suggest_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    return ''.join(random.choice(characters) for _ in range(length))

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        password = request.form.get("password")
        result = check_strength(password)
    return render_template("index.html", result=result)

@app.route("/suggest", methods=["POST"])
def suggest():
    suggestion = suggest_password()
    return render_template("index.html", suggestion=suggestion)

if __name__ == "__main__":
    app.run(debug=True)

   

  

