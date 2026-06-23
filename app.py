import sys
import os
import uuid
from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

sys.path.append("hire_sense_AI")
from read_resume import extract_text
from main import run_pipeline

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- DATABASE ----------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---------------- USER MODEL ----------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

# ---------------- INIT DB ----------------
with app.app_context():
    db.create_all()

# ---------------- FILE UPLOAD ----------------
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"pdf", "docx", "doc", "txt"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        fullname = request.form["fullname"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirm_password"]

        if password != confirm:
            return render_template("signup.html", error="Passwords do not match")

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template("signup.html", error="Username already exists")

        hashed_password = generate_password_hash(password)

        new_user = User(
            fullname=fullname,
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

    return render_template("signup.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user"] = username
            return redirect("/")
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    # 1. Delete all uploaded files associated with this user
    uploaded_files = session.get('uploaded_files', [])
    
    for filename in uploaded_files:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # 2. If the file exists on the server, delete it
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted file: {filename}")
        except Exception as e:
            print(f"Error deleting file {filename}: {e}")

    # 3. Clear all session variables and log out the user
    session.pop('uploaded_files', None)
    session.pop('uploaded_resume', None)
    session.pop('user', None)
    return redirect(url_for('login'))
# ---------------- UPLOAD ----------------
@app.route("/upload", methods=["GET", "POST"])
def upload_resume():

    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        if "resume" not in request.files:
            return render_template("upload_resume.html", error="No file selected")

        file = request.files["resume"]

        if file.filename == "":
            return render_template("upload_resume.html", error="No file selected")

        if not allowed_file(file.filename):
            return render_template("upload_resume.html", error="Invalid file type")

        filename = str(uuid.uuid4()) + "_" + file.filename
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # Track uploaded file in session for cleanup on logout
        if 'uploaded_files' not in session:
            session['uploaded_files'] = []
        session['uploaded_files'].append(filename)
        session.modified = True

        text = extract_text(filepath)
        result = run_pipeline(text)

        if not result:
            return render_template("upload_resume.html", error="AI failed")

        return render_template(
            "results.html",
            filename=file.filename,
            result=text,
            category=result["category"],
            skills=result["skills"],
            jobs=result["jobs"]
        )

    return render_template("upload_resume.html")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)