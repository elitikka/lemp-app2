from flask import Flask, jsonify, request
import mysql.connector
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

@app.route("/api/health")
def health():
  try:
    connection = get_db_connection()
    connection.close()
    return jsonify({ "status": "healthy", "db": "healthy" })
  except Exception as e:
    return jsonify({ "status": "Failed", "db": f"error: {e}"}), 500 # Muokattu, jotta mahdolliset virheet näkyy
  
@app.route('/api/users')
def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/init-db')
def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100)
            )
        """)
        cursor.execute("""
            INSERT INTO users (name, email) VALUES
            ('John Doe', 'john@example.com'),
            ('Jane Smith', 'jane@example.com')
        """)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Database initialized"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/add-user', methods=['POST']) # Lisätty ominaisuus: Lisää käyttäjä
def add_user():
   try:
      data = request.get_json() # Hae Frontendistä annettu tieto (nimi ja säpö)
      name = data.get("name")
      email = data.get("email")
      conn = get_db_connection()
      cursor = conn.cursor()
      # Lisää tietokantaan käyttäjä annetulla nimellä ja säpöllä
      cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
      conn.commit()
      cursor.close()
      conn.close()
      return jsonify({"message": "User added succesfully"})
   except Exception as e:
      return jsonify({ "status": "Failed", "adduser": f"error: {e}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)