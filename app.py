import os

import pymysql
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for

# vai ler o arquivo .env (DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
load_dotenv()

app = Flask(__name__)

PERSONAGENS = [
    {
        "nome": "Manny Ribera",
        "descricao": "Amigo e parceiro de Tony durante grande parte da história. "
                     "Com ele, Tony compartilha momentos de lealdade, amizade e também de tragédias.",
    },
    {
        "nome": "Frank Lopez",
        "descricao": "Um dos primeiros chefes de Tony no mundo do crime e uma "
                     "figura importante para a ascensão do personagem.",
    },
    {
        "nome": "Elvira Hancock",
        "descricao": "Personagem que passa a fazer parte da vida de Tony após "
                     "diversos conflitos e que acaba se tornando sua esposa.",
    },
    {
        "nome": "Alejandro Sosa",
        "descricao": "Um poderoso traficante de drogas que possui uma relação "
                     "importante com Tony durante o desenvolvimento da história.",
    },
]


def get_connection():
    """Abre uma conexão nova com o MySQL usando só variáveis do .env."""
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tony")
def tony():
    return render_template("tony.html")


@app.route("/enredo")
def enredo():
    return render_template("enredo.html")


@app.route("/personagens")
def personagens():
    return render_template("personagens.html", personagens=PERSONAGENS)


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"].strip()
        email = request.form["email"].strip()
        personagem = request.form["personagem_favorito"]
        comentario = request.form.get("comentario", "").strip()

        conn = get_connection()
        try:
            with conn.cursor() as cur:
                # consulta parametrizada (%s) -> protege contra SQL Injection
                cur.execute(
                    "INSERT INTO fas (nome, email, personagem_favorito, comentario) "
                    "VALUES (%s, %s, %s, %s)",
                    (nome, email, personagem, comentario),
                )
            conn.commit()
        finally:
            conn.close()

        return redirect(url_for("listar", ok=1))

    opcoes = ["Tony Montana"] + [p["nome"] for p in PERSONAGENS]
    return render_template("cadastro.html", opcoes=opcoes)


@app.route("/listar")
def listar():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, nome, email, personagem_favorito, comentario, criado_em "
                "FROM fas ORDER BY id DESC"
            )
            registros = cur.fetchall()
    finally:
        conn.close()

    return render_template("listar.html", registros=registros)


if __name__ == "__main__":
    # sem debug=True: com host 0.0.0.0 o debugger ficaria exposto na internet
    app.run(host="0.0.0.0", port=5000)