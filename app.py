from flask import Flask, render_template, request, redirect, jsonify, session, url_for, send_from_directory, abort
from functools import wraps
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import re
import sqlite3
import uuid
from load_sql_data import load_data_from_sql
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ============================================================
# SECURITY CONFIG (from environment variables)
# ============================================================
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-local-secret-change-me")

# Uploads (contact form attachments)
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
MAX_ATTACHMENT_BYTES = 2 * 1024 * 1024  # 2 MB
ALLOWED_ATTACHMENT_EXTENSIONS = {
    # images
    "jpg", "jpeg", "png", "gif", "webp", "bmp",
    # pdf
    "pdf",
    # documents
    "doc", "docx", "odt", "rtf",
    # text
    "txt", "csv", "md", "log",
}

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    # SESSION_COOKIE_SECURE=True,  # enable after HTTPS deploy on Render
    PERMANENT_SESSION_LIFETIME=timedelta(
        minutes=int(os.environ.get("SESSION_TIMEOUT_MINUTES", "10"))
    ),
    MAX_CONTENT_LENGTH=MAX_ATTACHMENT_BYTES + (512 * 1024),  # file + form overhead
    UPLOAD_FOLDER=UPLOAD_FOLDER,
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


def _allowed_attachment(filename: str) -> bool:
    if not filename or "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[-1].lower()
    return ext in ALLOWED_ATTACHMENT_EXTENSIONS


def _save_attachment(file_storage):
    """Validate and save uploaded file. Returns (stored_name, original_name) or (None, None)."""
    if not file_storage or not file_storage.filename:
        return None, None

    original = secure_filename(file_storage.filename)
    if not original or not _allowed_attachment(original):
        return False, None  # signal invalid type

    # size check (Content-Length may already enforce; also check stream)
    file_storage.stream.seek(0, os.SEEK_END)
    size = file_storage.stream.tell()
    file_storage.stream.seek(0)
    if size > MAX_ATTACHMENT_BYTES:
        return False, "size"  # signal too large

    if size == 0:
        return None, None

    ext = original.rsplit(".", 1)[-1].lower()
    stored = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:10]}.{ext}"
    dest = os.path.join(app.config["UPLOAD_FOLDER"], stored)
    file_storage.save(dest)
    return stored, original


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
            created_at TEXT NOT NULL,
            attachment_stored TEXT,
            attachment_original TEXT
        )
        """
    )
    # Migrate older DBs that lack attachment columns
    cols = {row[1] for row in conn.execute("PRAGMA table_info(messages)").fetchall()}
    if "attachment_stored" not in cols:
        conn.execute("ALTER TABLE messages ADD COLUMN attachment_stored TEXT")
    if "attachment_original" not in cols:
        conn.execute("ALTER TABLE messages ADD COLUMN attachment_original TEXT")
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

        attachment_stored = None
        attachment_original = None
        file = request.files.get("attachment")

        if not name or not phone or not email or not message:
            error = "Please fill Name, Phone Number, Email and Message."
        elif not is_valid_email(email):
            error = "Please enter a valid email address."
        elif not is_valid_phone(phone):
            error = "Please enter a valid phone number."
        elif len(message) < 10:
            error = "Message is too short."
        else:
            # Optional attachment validation / save
            if file and file.filename:
                stored, original = _save_attachment(file)
                if stored is False:
                    if original == "size":
                        error = "Attachment is too large. Maximum size is 2 MB."
                    else:
                        error = "Attachment type not allowed. Use image, PDF, document, or text file."
                else:
                    attachment_stored, attachment_original = stored, original

            if not error:
                ip = _client_ip()

                # Save to DB
                conn = sqlite3.connect("messages.db")
                conn.execute(
                    """
                    INSERT INTO messages
                    (name, phone, email, subject, message, ip_address, created_at,
                     attachment_stored, attachment_original)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        name, phone, email, subject, message, ip,
                        datetime.now().isoformat(),
                        attachment_stored, attachment_original,
                    ),
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
                    if attachment_original:
                        f.write(f"Attachment: {attachment_original} -> {attachment_stored}\n")
                    f.write(f"Message:\n{message}\n")

                return redirect("/thankyou")

    return render_template("contact.html", data=data, error=error)


@app.errorhandler(413)
def request_entity_too_large(e):
    data = get_data()
    return render_template(
        "contact.html",
        data=data,
        error="Attachment is too large. Maximum size is 2 MB.",
    ), 413


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
        SELECT id, name, phone, email, subject, message, created_at,
               attachment_stored, attachment_original
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
        a.logout, a.attach {{
          color:#60a5fa;
          text-decoration:none;
          font-size:14px;
        }}
        a.logout {{ float:right; }}
        .attach-row {{ margin-top:10px; font-size:13px; }}
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
            attach_html = ""
            if r["attachment_stored"] and r["attachment_original"]:
                attach_html = (
                    f'<div class="attach-row">Attachment: '
                    f'<a class="attach" href="{url_for("download_attachment", message_id=r["id"])}">'
                    f'{r["attachment_original"]}</a></div>'
                )
            # Basic escape for display (message may still need stronger escaping)
            msg = (r["message"] or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            name = (r["name"] or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            subj = (r["subject"] or "-").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            html += f"""
            <div class="card">
              <div class="meta">
                <b>#{r['id']}</b> | {r['created_at']}<br>
                <b>{name}</b> | {r['phone'] or '-'} | {r['email']}<br>
                Subject: {subj}
              </div>
              <div class="msg">{msg}</div>
              {attach_html}
            </div>
            """

    html += "</body></html>"
    return html


@app.route("/view-webpage-messages/attachment/<int:message_id>")
@login_required
def download_attachment(message_id):
    conn = sqlite3.connect("messages.db")
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT attachment_stored, attachment_original FROM messages WHERE id = ?",
        (message_id,),
    ).fetchone()
    conn.close()

    if not row or not row["attachment_stored"]:
        abort(404)

    stored = row["attachment_stored"]
    # Prevent path traversal
    if "/" in stored or "\\" in stored or ".." in stored:
        abort(404)

    folder = app.config["UPLOAD_FOLDER"]
    if not os.path.isfile(os.path.join(folder, stored)):
        abort(404)

    return send_from_directory(
        folder,
        stored,
        as_attachment=True,
        download_name=row["attachment_original"] or stored,
    )


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