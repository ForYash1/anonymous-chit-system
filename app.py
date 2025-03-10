import psycopg2
import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Get database URL from Render
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://anonymous_chit_db_user:geZ4XThmKf0uOcc74UQTo693mHMPK8kN@dpg-cv7ebeqj1k6c73ecf9q0-a/anonymous_chit_db")

# Connect to PostgreSQL
def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

# Initialize database (run only once)
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chits (
            id SERIAL PRIMARY KEY,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        message = request.form.get("message")
        if message:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO chits (message) VALUES (%s)", (message,))
            conn.commit()
            cursor.close()
            conn.close()
        return redirect("/")
    return render_template("index.html")

@app.route("/admin")
def admin():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chits")
    messages = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("admin.html", messages=messages)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
