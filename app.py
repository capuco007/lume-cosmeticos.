import os, re, sqlite3
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "lume.db")
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "troque-esta-chave-antes-de-publicar-9d7f2c1a")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    with sqlite3.connect(DB_PATH) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL COLLATE NOCASE UNIQUE,
                phone TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.commit()

@app.context_processor
def inject_user():
    return {"current_user": session.get("user")}

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user"):
            flash("Entre na sua conta para acessar essa página.", "info")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped

PRODUCTS = [
    {"id": 1, "name": "Sérum Aurora", "category": "Rosto", "description": "Hidratação leve para iluminar sua rotina.", "price": 79.90, "tone": "coral", "tag": "Mais vendido"},
    {"id": 2, "name": "Creme Botânico", "category": "Rosto", "description": "Toque macio e cuidado diário para a pele.", "price": 89.90, "tone": "sage", "tag": "Novo"},
    {"id": 3, "name": "Óleo Rosé", "category": "Corpo", "description": "Um ritual nutritivo com acabamento delicado.", "price": 64.90, "tone": "pink", "tag": "Favorito"},
    {"id": 4, "name": "Essência Dourada", "category": "Corpo", "description": "Perfume suave para acompanhar seu dia.", "price": 99.90, "tone": "gold", "tag": "Especial"},
    {"id": 5, "name": "Máscara de Brilho", "category": "Cabelo", "description": "Cuidado intensivo para fios radiantes.", "price": 74.90, "tone": "sage", "tag": ""},
    {"id": 6, "name": "Bálsamo Calmante", "category": "Rosto", "description": "Conforto e carinho nos pequenos detalhes.", "price": 54.90, "tone": "pink", "tag": ""},
    {"id": 7, "name": "Loção Suave", "category": "Corpo", "description": "Hidratação confortável para todos os dias.", "price": 69.90, "tone": "coral", "tag": ""},
    {"id": 8, "name": "Sérum Capilar", "category": "Cabelo", "description": "Finalização leve para um toque sedoso.", "price": 84.90, "tone": "gold", "tag": ""}
]

@app.route("/")
def index():
    return render_template("index.html", products=PRODUCTS)

@app.route("/cadastro", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        if len(name) < 2:
            flash("Informe seu nome completo.", "error")
        elif not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            flash("Informe um e-mail válido.", "error")
        elif len(re.sub(r"\D", "", phone)) < 10:
            flash("Informe um telefone com DDD.", "error")
        elif len(password) < 8:
            flash("A senha precisa ter pelo menos 8 caracteres.", "error")
        else:
            try:
                get_db().execute(
                    "INSERT INTO customers (name,email,phone,password_hash) VALUES (?,?,?,?)",
                    (name, email, phone, generate_password_hash(password))
                )
                get_db().commit()
                flash("Cadastro realizado! Agora entre com seu e-mail e senha.", "success")
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                flash("Esse e-mail já está cadastrado. Faça login.", "error")
    return render_template("auth.html", mode="register")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = get_db().execute("SELECT * FROM customers WHERE email = ?", (email,)).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user"] = {"id": user["id"], "name": user["name"], "email": user["email"], "phone": user["phone"]}
            flash("Login realizado. Que bom ter você aqui!", "success")
            return redirect(url_for("account"))
        flash("E-mail ou senha incorretos.", "error")
    return render_template("auth.html", mode="login")

@app.route("/minha-conta")
@login_required
def account():
    return render_template("account.html")

@app.route("/sair", methods=["POST"])
def logout():
    session.clear()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
