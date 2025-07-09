from CONECTAR.funcaoConectar import conectar
from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/CadastroUsuario", methods=["GET"])
def listar_Cadastros():
    conn = conectar()
    #conn.execute("PRAGMA foreign_keys = ON") #ativa as chaves estrangeiras das tabelas (pois, não é ativado por padrão)
    cursor = conn.cursor()
    cursor.execute("SELECT IDCadastroUsuario, NomeUsuario, EmailUsuario,EmailUsuario FROM CadastroUsuario")
    dados = [
        {"id": row[0], "NomeUsuario": row[1], "EmailUsuario": row[2], "EmailUsuario": row[3]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(dados)

##ROTA INSERT
#############################################

from flask import request, jsonify, abort
@app.route("/CadastroUsuario", methods=["POST"])
def criar_usuario():
    dados = request.get_json(silent=True)
    if not dados:
        abort(400, description="JSON inválido ou ausente")

    # Validação de campos obrigatórios
    campos_obrigatorios = {"NomeUsuario", "EmailUsuario", "SenhaUsuario"}
    if not campos_obrigatorios.issubset(dados.keys()):
        abort(400, description=f"Campos obrigatórios: {', '.join(campos_obrigatorios)}")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO CadastroUsuario (NomeUsuario, EmailUsuario, SenhaUsuario) "
        "VALUES (?, ?, ?)",
        (dados["NomeUsuario"], dados["EmailUsuario"], dados["SenhaUsuario"])
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    # 201 Created + Location do recurso recém‑criado
    resposta = jsonify({"id": novo_id, **dados})
    resposta.status_code = 201
    resposta.headers["Location"] = f"/CadastroUsuario/{novo_id}"
    return resposta

if __name__ == "__main__":
    app.run(debug=True)

