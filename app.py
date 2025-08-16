from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "replace-with-a-secure-random-key"

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")
ADMIN_KEY = "admin123"  # Change this to something secret

BLOOD_GROUPS = [
    "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"
]


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    # donors table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            blood_group TEXT NOT NULL,
            contact TEXT NOT NULL,
            location TEXT NOT NULL,
            last_donated TEXT
        );
        """
    )
    # requests table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            blood_group TEXT NOT NULL,
            contact TEXT NOT NULL,
            location TEXT NOT NULL,
            urgency TEXT,
            note TEXT
        );
        """
    )
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        gender = request.form.get("gender", "").strip()
        blood_group = request.form.get("blood_group", "").strip()
        contact = request.form.get("contact", "").strip()
        location = request.form.get("location", "").strip()
        last_donated = request.form.get("last_donated", "").strip()

        # Basic validation
        errors = []
        if not name: errors.append("Name is required")
        if not age.isdigit(): errors.append("Valid age is required")
        if gender not in ["Male", "Female", "Other"]: errors.append("Select a valid gender")
        if blood_group not in BLOOD_GROUPS: errors.append("Select a valid blood group")
        if not contact: errors.append("Contact is required")
        if not location: errors.append("Location is required")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("register.html", blood_groups=BLOOD_GROUPS)

        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO donors (name, age, gender, blood_group, contact, location, last_donated)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (name, int(age), gender, blood_group, contact, location, last_donated or None),
        )
        conn.commit()
        conn.close()
        flash("Donor registered successfully!", "success")
        return redirect(url_for("register"))

    return render_template("register.html", blood_groups=BLOOD_GROUPS)


@app.route("/search", methods=["GET", "POST"])
def search():
    results = []
    selected_group = request.values.get("blood_group", "")
    location = request.values.get("location", "").strip()

    if request.method == "POST":
        q = "SELECT * FROM donors WHERE 1=1"
        params = []
        if selected_group in BLOOD_GROUPS:
            q += " AND blood_group = ?"
            params.append(selected_group)
        if location:
            q += " AND location LIKE ?"
            params.append(f"%{location}%")

        conn = get_conn()
        cur = conn.cursor()
        cur.execute(q, params)
        results = cur.fetchall()
        conn.close()

        if not results:
            flash("No donors found for the given filters.", "warning")

    return render_template("search.html", blood_groups=BLOOD_GROUPS, results=results, selected_group=selected_group, location=location)


@app.route("/request", methods=["GET", "POST"])
def request_blood():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        blood_group = request.form.get("blood_group", "").strip()
        contact = request.form.get("contact", "").strip()
        location = request.form.get("location", "").strip()
        urgency = request.form.get("urgency", "").strip()
        note = request.form.get("note", "").strip()

        errors = []
        if not name: errors.append("Name is required")
        if blood_group not in BLOOD_GROUPS: errors.append("Select a valid blood group")
        if not contact: errors.append("Contact is required")
        if not location: errors.append("Location is required")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("request.html", blood_groups=BLOOD_GROUPS)

        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO requests (name, blood_group, contact, location, urgency, note)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (name, blood_group, contact, location, urgency or None, note or None),
        )
        conn.commit()
        conn.close()
        flash("Blood request submitted!", "success")
        return redirect(url_for("request_blood"))

    return render_template("request.html", blood_groups=BLOOD_GROUPS)


@app.route("/admin", methods=["GET", "POST"])
def admin():
    # Simple key-based access (no sessions to keep code minimal)
    provided_key = request.values.get("key", "").strip()

    if request.method == "POST" and not provided_key:
        provided_key = request.form.get("key", "").strip()

    if provided_key != ADMIN_KEY:
        # Show minimal login form
        flash("Enter admin key to view dashboard.", "info")
        return render_template("admin.html", authorized=False)

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM donors ORDER BY id DESC")
    donors = cur.fetchall()
    cur.execute("SELECT * FROM requests ORDER BY id DESC")
    reqs = cur.fetchall()
    conn.close()

    return render_template("admin.html", authorized=True, donors=donors, reqs=reqs)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)