import os

import mysql.connector
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, session

from functools import wraps
from werkzeug.security import check_password_hash

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

if not app.secret_key:
    raise RuntimeError("FLASK_SECRET_KEY is missing from .env")


""" This function establishes a connection to the MySQL database using the mysql.connector library.
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "portfolio_db")
    )
"""

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        ssl_disabled=False
    )

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        flash("Please fill in all the fields.", "error")
        return redirect(url_for("home") + "#contact")

    if len(name) > 100 or len(email) > 255 or len(message) > 5000:
        flash("Your submission is too long.", "error")
        return redirect(url_for("home") + "#contact")

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        sql = """
            INSERT INTO contact_messages (name, email, message)
            VALUES (%s, %s, %s)
        """

        cursor.execute(sql, (name, email, message))
        connection.commit()

        flash("Your message was sent successfully!", "success")

    except mysql.connector.Error:
        app.logger.exception("Database operation failed")
        flash(
            "Unable to send your message right now. Please try again later.",
            "error"
        )

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

    return redirect(url_for("home") + "#contact")

def admin_required(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))

        return view_function(*args, **kwargs)

    return wrapper

@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        stored_username = os.getenv("ADMIN_USERNAME", "")
        stored_hash = os.getenv("ADMIN_PASSWORD_HASH", "")

        if (
            stored_username
            and stored_hash
            and username == stored_username
            and check_password_hash(stored_hash, password)
        ):
            session.clear()
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))

        flash("Invalid username or password.", "error")

    return render_template("admin_login.html")

@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, name, email, message, created_at
            FROM contact_messages
            ORDER BY created_at DESC
            LIMIT 500
        """)

        messages = cursor.fetchall()

        return render_template(
            "admin_dashboard.html",
            messages=messages
        )

    except mysql.connector.Error:
        app.logger.exception("Could not load contact messages")
        return "Unable to load messages. Check the server logs.", 500

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

@app.route("/admin/logout", methods=["POST"])
@admin_required
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))

if __name__ == "__main__":
    app.run(debug=True)