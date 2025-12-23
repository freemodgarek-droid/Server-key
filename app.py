from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

ADMIN_PW = "admin123"   # ganti password admin
DB = "keys.db"

# init database
conn = sqlite3.connect(DB)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS keys (key TEXT PRIMARY KEY)")
conn.commit()
conn.close()

def db():
    return sqlite3.connect(DB)

@app.route("/")
def home():
    return "SERVER KEY AKTIF"

@app.route("/check")
def check():
    key = request.args.get("key")
    conn = db()
    c = conn.cursor()
    c.execute("SELECT key FROM keys WHERE key=?", (key,))
    data = c.fetchone()
    conn.close()
    return jsonify(status="valid" if data else "invalid")

@app.route("/add", methods=["POST"])
def add():
    if request.form.get("pw") != ADMIN_PW:
        return jsonify(status="error", msg="password salah")
    key = request.form.get("key")
    try:
        conn = db()
        c = conn.cursor()
        c.execute("INSERT INTO keys VALUES (?)", (key,))
        conn.commit()
        conn.close()
        return jsonify(status="success", key=key)
    except:
        return jsonify(status="error", msg="key sudah ada")

app.run(host="0.0.0.0", port=8080)