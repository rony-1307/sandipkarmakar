from flask import Flask, render_template, request, redirect, jsonify, session, url_for
from functools import wraps
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re
import sqlite3
from load_sql_data import load_data_from_sql
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ============================================================
# SECURITY CONFIG (from environment variables)
# ============================================================
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-local-secret-change-me")

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    # SESSION_COOKIE_SECURE=True,  # enable after HTTPS deploy on Render
    PERMANENT_SESSION_LIFETIME=timedelta(
        minutes=int(os.environ.get("SESSION_TIMEOUT_MINUTES", "10"))
    ),
)

# Admin login from environment (set these on Render)
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")       # local default only
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")    # local default only
ADMIN_PASSWORD_HASH = generate_password_hash(ADMIN_PASSWORD)

SESSION_TIMEOUT_MINUTES = int(os.environ.get("SESSION_TIMEOUT_MINUTES", "10"))
MAX_LOGIN_ATTEMPTS = int(os.environ.get("MAX_LOGIN_ATTEMPTS", "2"))
LOCK_MINUTES = int(os.environ.get("LOCK_MINUTES", "30"))

# ip -> {"count": int, "locked_until": datetime|None}
login_attempts = {}


# ============================================================
# BASIC HELPERS
# ============================================================
def get_data():
    return load_data_from_sql()


def clean_text(text: str, max_len: int = 2000) -> str:
    if not text:
        return ""
    text = text.strip()
    text = re.sub(r"<[^>]*>", "", text)
    return text[:max_len]


def is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def is_valid_phone(phone: str) -> bool:
    if not phone:
        return False
    phone = phone.strip()
    pattern = r"^\+?[0-9\s\-\(\)]{8,20}$"
    return re.match(pattern, phone) is not None


def _client_ip():
    return request.headers.get("X-Forwarded-For", request.remote_addr)


def _is_locked(ip: str) -> bool:
    data = login_attempts.get(ip)
    if not data or not data.get("locked_until"):
        return False
    if datetime.now() >= data["locked_until"]:
        login_attempts[ip] = {"count": 0, "locked_until": None}
        return False
    return True


def _register_failed_login(ip: str):
    data = login_attempts.get(ip, {"count": 0, "locked_until": None})
    data["count"] += 1
    if data["count"] >= MAX_LOGIN_ATTEMPTS:
        data["locked_until"] = datetime.now() + timedelta(minutes=LOCK_MINUTES)
        data["count"] = 0
    login_attempts[ip] = data


def _register_success_login(ip: str):
    login_attempts[ip] = {"count": 0, "locked_until": None}


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("messages_login"))

        login_time = session.get("login_time")
        if not login_time:
            session.clear()
            return redirect(url_for("messages_login"))

        try:
            lt = datetime.fromisoformat(login_time)
        except Exception:
            session.clear()
            return redirect(url_for("messages_login"))

        if datetime.now() - lt > timedelta(minutes=SESSION_TIMEOUT_MINUTES):
            session.clear()
            return redirect(url_for("messages_login"))

        # refresh session activity
        session["login_time"] = datetime.now().isoformat()
        return f(*args, **kwargs)
    return decorated


# ============================================================
# MESSAGES DATABASE
# ============================================================
def init_messages_db():
    conn = sqlite3.connect("messages.db")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT,
            message TEXT NOT NULL,
            ip_address TEXT,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


init_messages_db()


# ============================================================
# PUBLIC PAGES
# ============================================================
@app.route("/")
def index():
    data = get_data()
    return render_template("index.html", data=data)


@app.route("/about")
def about():
    data = get_data()
    return render_template("about.html", data=data)


@app.route("/education")
def education():
    data = get_data()
    return render_template("education.html", data=data)


@app.route("/experience")
def experience():
    data = get_data()
    return render_template("experience.html", data=data)


@app.route("/publications")
def publications():
    data = get_data()
    return render_template("publications.html", data=data)


@app.route("/projects")
def projects():
    data = get_data()
    return render_template("projects.html", data=data)


@app.route("/achievements")
def achievements():
    data = get_data()
    return render_template("achievements.html", data=data)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    data = get_data()
    error = None

    if request.method == "POST":
        # Honeypot
        if request.form.get("website"):
            return redirect("/contact")

        name = clean_text(request.form.get("name", ""), 100)
        phone = clean_text(request.form.get("phone", ""), 20)
        email = clean_text(request.form.get("email", ""), 150).lower()
        subject = clean_text(request.form.get("user_subject", ""), 200)
        message = clean_text(request.form.get("message", ""), 3000)

        if not name or not phone or not email or not message:
            error = "Please fill Name, Phone Number, Email and Message."
        elif not is_valid_email(email):
            error = "Please enter a valid email address."
        elif not is_valid_phone(phone):
            error = "Please enter a valid phone number."
        elif len(message) < 10:
            error = "Message is too short."
        else:
            ip = _client_ip()

            # Save to DB
            conn = sqlite3.connect("messages.db")
            conn.execute(
                """
                INSERT INTO messages
                (name, phone, email, subject, message, ip_address, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (name, phone, email, subject, message, ip, datetime.now().isoformat()),
            )
            conn.commit()
            conn.close()

            # Save to log file
            with open("messages_log.txt", "a", encoding="utf-8") as f:
                f.write(f"\n{'=' * 50}\n")
                f.write(f"Time   : {datetime.now()}\n")
                f.write(f"Name   : {name}\n")
                f.write(f"Phone  : {phone}\n")
                f.write(f"Email  : {email}\n")
                f.write(f"Subject: {subject}\n")
                f.write(f"IP     : {ip}\n")
                f.write(f"Message:\n{message}\n")

            return redirect("/thankyou")

    return render_template("contact.html", data=data, error=error)


@app.route("/thankyou")
def thankyou():
    data = get_data()
    return render_template("thankyou.html", data=data)


# ============================================================
# SECURE MESSAGES INBOX (User ID + Password)
# ============================================================
@app.route("/view-webpage-messages/login", methods=["GET", "POST"])
def messages_login():
    ip = _client_ip()
    error = None

    if _is_locked(ip):
        error = "Too many attempts. Try again later."
    elif request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        valid_user = username == ADMIN_USERNAME
        valid_pass = check_password_hash(ADMIN_PASSWORD_HASH, password)

        if valid_user and valid_pass:
            session.clear()
            session["admin_logged_in"] = True
            session["login_time"] = datetime.now().isoformat()
            session.permanent = True
            _register_success_login(ip)
            return redirect(url_for("view_messages"))
        else:
            _register_failed_login(ip)
            error = "Invalid username or password"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Messages Login</title>
      <style>
        body {{
          font-family: Arial, sans-serif;
          background:#0f172a;
          color:#fff;
          display:flex;
          justify-content:center;
          align-items:center;
          min-height:100vh;
          margin:0;
        }}
        .box {{
          background:#1e293b;
          padding:24px;
          border-radius:12px;
          width:90%;
          max-width:360px;
        }}
        input, button {{
          width:100%;
          padding:12px;
          margin-top:10px;
          border-radius:8px;
          border:none;
          font-size:16px;
          box-sizing:border-box;
        }}
        button {{
          background:#2563eb;
          color:#fff;
          font-weight:bold;
          cursor:pointer;
        }}
        .error {{
          color:#f87171;
          margin-top:10px;
        }}
      </style>
    </head>
    <body>
      <div class="box">
        <h2>Messages Login</h2>
        <form method="POST" autocomplete="off">
          <input type="text" name="username" placeholder="User ID" required>
          <input type="password" name="password" placeholder="Password" required>
          <button type="submit">Login</button>
        </form>
        {"<p class='error'>" + error + "</p>" if error else ""}
      </div>
    </body>
    </html>
    """


@app.route("/view-webpage-messages")
@login_required
def view_messages():
    conn = sqlite3.connect("messages.db")
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """
        SELECT id, name, phone, email, subject, message, created_at
        FROM messages
        ORDER BY id DESC
        """
    ).fetchall()
    conn.close()

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Messages</title>
      <style>
        body {{
          font-family: Arial, sans-serif;
          background:#0f172a;
          color:#e2e8f0;
          margin:0;
          padding:16px;
        }}
        h1 {{ font-size:22px; }}
        .card {{
          background:#1e293b;
          border-radius:12px;
          padding:14px;
          margin-bottom:14px;
        }}
        .meta {{
          color:#94a3b8;
          font-size:13px;
          margin-bottom:8px;
        }}
        .msg {{
          white-space:pre-wrap;
          line-height:1.5;
        }}
        a.logout {{
          color:#60a5fa;
          text-decoration:none;
          float:right;
          font-size:14px;
        }}
      </style>
    </head>
    <body>
      <h1>
        Inbox ({len(rows)})
        <a class="logout" href="{url_for('messages_logout')}">Logout</a>
      </h1>
    """

    if not rows:
        html += "<p>No messages yet.</p>"
    else:
        for r in rows:
            html += f"""
            <div class="card">
              <div class="meta">
                <b>#{r['id']}</b> | {r['created_at']}<br>
                <b>{r['name']}</b> | {r['phone'] or '-'} | {r['email']}<br>
                Subject: {r['subject'] or '-'}
              </div>
              <div class="msg">{r['message']}</div>
            </div>
            """

    html += "</body></html>"
    return html


@app.route("/view-webpage-messages/logout")
def messages_logout():
    session.clear()
    return redirect(url_for("messages_login"))


# ============================================================
# 404
# ============================================================
@app.errorhandler(404)
def page_not_found(e):
    data = get_data()
    return render_template("404.html", data=data), 404


# ============================================================
# RUN
# ============================================================
if __name__ == "__main__":
    data = get_data()
    print("🚀 Sandip Karmakar Portfolio")
    print(f"✅ Loaded data for: {data['personal']['name']}")
    print(f"   Experience : {len(data['experience'])}")
    print(f"   Education  : {len(data['education'])}")
    print(f"   Projects   : {len(data['projects'])}")
    print(f"   Publications: {len(data['publications'])}")

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)