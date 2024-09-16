from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# PostgreSQL database connection details
DB_HOST = "localhost"
DB_NAME = "login_db"
DB_USER = "postgres"
DB_PASS = "password"
PORT = "5432"


def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=PORT
    )
    return conn

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    cur = conn.cursor()

    # Check if the user already exists
    cur.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
    user = cur.fetchone()

    if user:
        # If the user exists, log them in
        cur.close()
        conn.close()
        return f"Welcome, {username}!"
    else:
        # If the user doesn't exist, insert them into the database
        cur.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
        conn.commit()  # Commit the transaction to the database
        
        cur.close()
        conn.close()
        flash('User registered successfully! Please log in.')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)