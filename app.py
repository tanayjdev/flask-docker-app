import os
import psycopg2
from flask import Flask

app = Flask(__name__)

# database container ka hostname
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


@app.route("/")
def home():
    conn = get_connection()
    cur = conn.cursor()

    # table create karo agar nahi hai
    cur.execute("CREATE TABLE IF NOT EXISTS visits (count INT)")

    cur.execute("SELECT count FROM visits")
    row = cur.fetchone()

    if row is None:
        cur.execute("INSERT INTO visits VALUES (1)")
        count = 1
    else:
        count = row[0] + 1
        cur.execute("UPDATE visits SET count = %s", (count,))

    conn.commit()

    cur.close()
    conn.close()

    return f"Page visited {count} times!"


# Health endpoint
@app.route("/health")
def health():
    try:
        conn = get_connection()
        conn.close()
        return {"status": "healthy", "database": "connected"}, 200
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
