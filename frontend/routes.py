from flask import Blueprint, render_template


frontend_bp = Blueprint(
    "frontend",
    __name__
)


# ============================================================
# INDEX
# ============================================================

@frontend_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# ============================================================
# LOGIN
# ============================================================

@frontend_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


# ============================================================
# CADASTRO
# ============================================================

@frontend_bp.route("/cadastro", methods=["GET"])
def cadastro_page():
    return render_template("cadastro.html")


# ============================================================
# HOME
# ============================================================

@frontend_bp.route("/home", methods=["GET"])
def home():
    return render_template("home.html")

# ============================================================
# DETALHE
# ============================================================
@frontend_bp.route("/detalhe")
def detalhe_page():
    return render_template("detalhe.html")
