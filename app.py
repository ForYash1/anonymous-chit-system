from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    with sqlite3.connect("chits.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS chits (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            message TEXT NOT NULL)''')
        conn.commit()

# Home page (Message Submission)
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        message = request.form.get("message")
        if message:
            with sqlite3.connect("chits.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO chits (message) VALUES (?)", (message,))
                conn.commit()
        return redirect("/")
    return render_template("index.html")

# Admin Page (View Messages)
@app.route("/admin")
def admin():
    with sqlite3.connect("chits.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM chits")
        messages = cursor.fetchall()
    return render_template("admin.html", messages=messages)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
