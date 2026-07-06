import sqlite3
from datetime import datetime

from flask import Flask, g, redirect, render_template, request, url_for

app = Flask(__name__)

DATABASE = "relatos.db"

PROBLEMAS_DISPONIVEIS = [
    "OPÇÃO A",
    "OPÇÃO B",
    "OPÇÃO C",
    "OPÇÃO D",
    "OPÇÃO E",
    "OPÇÃO F",
]


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(DATABASE) as db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS relatos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                criado_em TEXT NOT NULL,
                novato_nome TEXT NOT NULL,
                turno TEXT NOT NULL,
                instrutor_nome TEXT NOT NULL,
                sistema_afetado TEXT NOT NULL,
                problemas TEXT NOT NULL,
                observacoes TEXT,
                status TEXT NOT NULL DEFAULT 'Pendente'
            )
            """
        )


@app.route("/")
def formulario():
    return render_template("form.html", problemas=PROBLEMAS_DISPONIVEIS)


@app.route("/enviar", methods=["POST"])
def enviar():
    novato_nome = request.form.get("novato_nome", "").strip()
    turno = request.form.get("turno", "").strip()
    instrutor_nome = request.form.get("instrutor_nome", "").strip()
    sistema_afetado = request.form.get("sistema_afetado", "").strip()
    problemas_marcados = request.form.getlist("problemas")
    observacoes = request.form.get("observacoes", "").strip()

    db = get_db()
    db.execute(
        """
        INSERT INTO relatos
            (criado_em, novato_nome, turno, instrutor_nome, sistema_afetado, problemas, observacoes, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'Pendente')
        """,
        (
            datetime.now().strftime("%d/%m/%Y %H:%M"),
            novato_nome,
            turno,
            instrutor_nome,
            sistema_afetado,
            ", ".join(problemas_marcados),
            observacoes,
        ),
    )
    db.commit()

    return redirect(url_for("formulario", enviado=1))


@app.route("/painel")
def painel():
    db = get_db()
    relatos = db.execute(
        "SELECT * FROM relatos ORDER BY id DESC"
    ).fetchall()
    return render_template("painel.html", relatos=relatos)


@app.route("/painel/resolver/<int:relato_id>", methods=["POST"])
def resolver(relato_id):
    db = get_db()
    novo_status = "Resolvido" if request.form.get("acao") == "resolver" else "Pendente"
    db.execute("UPDATE relatos SET status = ? WHERE id = ?", (novo_status, relato_id))
    db.commit()
    return redirect(url_for("painel"))


@app.route("/painel/finalizar_turno", methods=["POST"])
def finalizar_turno():
    db = get_db()
    db.execute("DELETE FROM relatos")
    db.execute("DELETE FROM sqlite_sequence WHERE name = 'relatos'")
    db.commit()
    return redirect(url_for("painel"))


init_db()

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
