from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import json

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullName TEXT,
        username TEXT UNIQUE,
        password TEXT,
        grade TEXT,
        status TEXT,
        internalId TEXT,
        unlockedLessons TEXT,
        scores TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return send_from_directory('.', 'index_modified.html')

@app.route('/register', methods=['POST'])
def register():

    data = request.json

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    try:

        cursor.execute("""
        INSERT INTO users
        (fullName, username, password, grade, status, internalId, unlockedLessons, scores)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['fullName'],
            data['username'],
            data['password'],
            data['grade'],
            'pending',
            data['internalId'],
            json.dumps([]),
            json.dumps({})
        ))

        conn.commit()
        conn.close()

        return jsonify({
            "success": True
        })

    except Exception as e:

        conn.close()

        return jsonify({
            "success": False,
            "message": "اسم المستخدم مستخدم مسبقاً"
        })

@app.route('/login', methods=['POST'])
def login():

    data = request.json

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM users
    WHERE username=? AND password=?
    """, (
        data['username'],
        data['password']
    ))

    user = cursor.fetchone()

    conn.close()

    if user:

        return jsonify({
            "success": True,
            "user": {
                "id": user[0],
                "fullName": user[1],
                "username": user[2],
                "grade": user[4],
                "status": user[5],
                "internalId": user[6],
                "unlockedLessons": json.loads(user[7]),
                "scores": json.loads(user[8])
            }
        })

    return jsonify({
        "success": False,
        "message": "بيانات الدخول غير صحيحة"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
