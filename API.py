from CONECTAR.funcaoConectar import conectar
from flask import Flask, jsonify
from flask import request

app = Flask(__name__)

#rota tabela fornecedor usuatio#
@app.route("/FornecedorProduto", methods=["GET"])
def listar_FornecedorProduto():
    conn = conectar()
    #conn.execute("PRAGMA foreign_keys = ON") #ativa as chaves estrangeiras das tabelas (pois, não é ativado por padrão)
    cursor = conn.cursor()
    cursor.execute("SELECT Cnpj, CodBarraFornecedor, InformeProdutoForn, NomeFornecedor, EndFornecedor FROM FornecedorProduto")
    dados = [
        {"Cnpj": row[0], "CodBarraFornecedor": row[1], "InformeProdutoForn": row[2], "NomeFornecedor": row[3], "EndFornecedor": row[4]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(dados)
#############################################
@app.route("/CadastroProdutoServico", methods=["GET"])
def Lista_CadastroProdutoServico():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT IdCadastroProduto, CodBarra, InformeProduto, Fornecedor, TipoFornecedor, Quantidade FROM CadastroProdutoServico")

    dados = [
        {"id": row[0], "CodBarra": row[1], "InformeProduto": row[2], "Fornecedor": row[3], "TipoFornecedor": row[4], "Quantidade": row[5]}
        for row in cursor.fetchall()
    ]

    conn.close()
    return jsonify(dados)

@app.route("/CadastroUsuario", methods=["GET"])
def Lista_Cadastro():
    
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT IDCadastroUsuario, NomeUsuario, SenhaUsuario, SetorUsuario FROM CadastroUsuario")
    dados = [
        {"id": row[0], "NomeUsuario": row[1], "SenhaUsuario": row[2], "SetorUsuario": row[3]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(dados)
<<<<<<< HEAD
#########rota login###############
@app.route("/login", methods=["GET"])
def login():
    nome = request.args.get("nome", "").strip()
    senha = request.args.get("senha", "").strip()
    setor = request.args.get("setor", "").strip()

    conn = conectar()
    cursor = conn.cursor()

    query = """
        SELECT IDCadastroUsuario, NomeUsuario, SetorUsuario
        FROM CadastroUsuario
        WHERE NomeUsuario = ? AND SenhaUsuario = ? AND SetorUsuario = ?
    """
    cursor.execute(query, (nome, senha, setor))
    usuario = cursor.fetchone()

    conn.close()

    if usuario:
        return jsonify({
            "login": True,
            "id": usuario[0],
            "nome": usuario[1],
            "setor": usuario[2]
        })
    else:
        return jsonify({"login": False})
    #################################
=======
>>>>>>> 70e64bd8f76495c20bd5ed9e9634aa9965e99bab

@app.route("/CadastroUsuario/buscarPorNome", methods=["GET"])
def buscar_usuario_por_nome():
    nome = request.args.get('nome', '').strip()

    conn = conectar()
    cursor = conn.cursor()

    query = """
        SELECT IDCadastroUsuario, NomeUsuario, SenhaUsuario, SetorUsuario
        FROM CadastroUsuario
        WHERE LOWER(NomeUsuario) LIKE LOWER(?)
    """
    cursor.execute(query, ('%' + nome + '%',))

    dados = [
        {"id": row[0], "NomeUsuario": row[1], "SenhaUsuario": row[2], "SetorUsuario": row[3]}
        for row in cursor.fetchall()
    ]

    conn.close()
    return jsonify(dados)

    
    ##ROTA DELETE
#############################################
from flask import jsonify, abort

@app.route("/CadastroUsuario/<int:id_usuario>", methods=["DELETE"])
def deletar_usuario(id_usuario):
    conn = conectar()
    cursor = conn.cursor()

    # tenta apagar o registro informado
    cursor.execute("DELETE FROM CadastroUsuario WHERE IDCadastroUsuario = ?", (id_usuario,))
    conn.commit()

    # cursor.rowcount informa quantas linhas foram afetadas
    if cursor.rowcount == 0:
        conn.close()
        # nenhum registro com esse ID → devolve 404
        abort(404, description="Usuário não encontrado")

    conn.close()
    # 204 = No Content (padrão para deleções bem‑sucedidas)
    return ({"mensagem": "Usuário deletado com sucesso"}), 200


from flask import request, jsonify, abort

##ROTA INSERT
#############################################
@app.route("/CadastroUsuario", methods=["POST"])
def criar_usuario():
    dados = request.get_json(silent=True)
    if not dados:
        abort(400, description="JSON inválido ou ausente")

    # Validação de campos obrigatórios
    campos_obrigatorios = {"NomeUsuario", "SenhaUsuario", "SetorUsuario"}
    if not campos_obrigatorios.issubset(dados.keys()):
        abort(400, description=f"Campos obrigatórios: {', '.join(campos_obrigatorios)}")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO CadastroUsuario (NomeUsuario, SenhaUsuario, SetorUsuario) "
        "VALUES (?, ?, ?)",
        (dados["NomeUsuario"], dados["SenhaUsuario"], dados["SetorUsuario"])
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    # 201 Created + Location do recurso recém‑criado
    resposta = jsonify({"id": novo_id, **dados})
    resposta.status_code = 201
    resposta.headers["Location"] = f"/CadastroUsuario/{novo_id}"
    return resposta

##ROTA UPDATE
#############################################
@app.route("/CadastroUsuario/<int:id_usuario>", methods=["PUT", "PATCH"])
def atualizar_usuario(id_usuario):
    dados = request.get_json(silent=True)
    if not dados:
        abort(400, description="JSON inválido ou ausente")

    # Para PUT, garanta que todos os campos estejam presentes
    if request.method == "PUT":
        campos_esperados = {"NomeUsuario", "SenhaUsuario", "SetorUsuario"}
        if not campos_esperados.issubset(dados.keys()):
            abort(400, description=f"PUT requer todos os campos: {', '.join(campos_esperados)}")

    # Monta dinamicamente o SQL somente com os campos enviados
    campos_validos = {"NomeUsuario", "SenhaUsuario", "SetorUsuario"}
    set_clauses = []
    valores = []
    for campo in campos_validos & dados.keys():
        set_clauses.append(f"{campo} = ?")
        valores.append(dados[campo])

    if not set_clauses:
        abort(400, description="Nenhum campo válido para atualizar")

    valores.append(id_usuario)  # último parâmetro é o WHERE

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE CadastroUsuario SET {', '.join(set_clauses)} WHERE IDCadastroUsuario = ?",
        tuple(valores)
    )
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        abort(404, description="Usuário não encontrado")

    conn.close()
    # 204 = No Content, mas você pode devolver 200 com o JSON atualizado se preferir
    return ("", 204)
##################ESTOQUE########################

#rota tabela EstoqueProduto#
@app.route("/EstoqueProduto", methods=["GET"])
def listar_EstoqueProduto():
    conn = conectar()
    #conn.execute("PRAGMA foreign_keys = ON") #ativa as chaves estrangeiras das tabelas (pois, não é ativado por padrão)
    cursor = conn.cursor()
    cursor.execute("SELECT IdEstoqueProduto, CodBarraProduto, FornecedorEst, NumeroNota,InformeProdutoEst, Unidade, EstMinimo, EstMaximo, ValidadeEst, PrecoCusto, PrecoVenda, QuantidadeEst, Desativa FROM EstoqueProduto")
    dados = [
        {"id": row[0], "CodBarraProduto": row[1], "FornecedorEst": row[2], "NumeroNota": row[3], "InformeProdutoEst": row[4], "Unidade": row[5], "EstMinimo": row[6], "EstMaximo": row[7], "ValidadeEst": row[8], "PrecoCusto": row[9], "PrecoVenda": row[10], "QuantidadeEst": row[11], "Desativa": row[12]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(dados)

<<<<<<< HEAD
########## CRIAR NA TABELA CADASTRO PRODUTOS ##########################
@app.route("/CadastroProdutoServico", methods=["POST"])
def criar_CadastroProdutoServico():
    dados = request.get_json()
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO CadastroProdutoServico (CodBarra, InformeProduto, Fornecedor, TipoFornecedor, Quantidade)
        VALUES (?, ?, ?, ?, ?)
    """, (
        dados["CodBarra"],
        dados["InformeProduto"],
        dados["Fornecedor"],
        dados["TipoFornecedor"],
        dados["Quantidade"]
    ))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Produto/serviço cadastrado com sucesso!"}), 201

# ----------------------- ATUALIZAR (UPDATE) -----------------------
@app.route("/CadastroProdutoServico/<int:id>", methods=["PUT"])
def atualizar_CadastroProdutoServico(id):
    dados = request.get_json()
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE CadastroProdutoServico
        SET CodBarra = ?, InformeProduto = ?, Fornecedor = ?, TipoFornecedor = ?, Quantidade = ?
        WHERE IdCadastroProduto = ?
    """, (
        dados["CodBarra"],
        dados["InformeProduto"],
        dados["Fornecedor"],
        dados["TipoFornecedor"],
        dados["Quantidade"],
        id
    ))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Produto/serviço atualizado com sucesso!"})

# ----------------------- EXCLUIR (DELETE) -----------------------
@app.route("/CadastroProdutoServico/<int:id>", methods=["DELETE"])
def excluir_CadastroProdutoServico(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM CadastroProdutoServico WHERE IdCadastroProduto = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Produto/serviço excluído com sucesso!"})
#---------------------------------#
if __name__ == "__main__":
    app.run(debug=False)
=======



################ CadastroProdutoServico EXIBIR ##################
@app.route("/CadastroProdutoServico", methods=["GET"])
def listar_CadastrosProdutoServico():
    conn = conectar()
    #conn.execute("PRAGMA foreign_keys = ON") #ativa as chaves estrangeiras das tabelas (pois, não é ativado por padrão)
    cursor = conn.cursor()
    cursor.execute("SELECT IdCadastroProduto, CodBarra, InformeProduto, Fornecedor,TipoFornecedor, Quantidade FROM CadastroProdutoServico")
    dados = [
        {"id": row[0], "CodBarra": row[1], "InformeProduto": row[2], "Fornecedor": row[3], "TipoFornecedor": row[4], "Quantidade": row[5]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(dados)
>>>>>>> 70e64bd8f76495c20bd5ed9e9634aa9965e99bab


from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def conectar():
    return sqlite3.connect('seu_banco.db')

@app.route("/CadastroProdutoServico/buscarPorCodigo", methods=["GET"])
def buscar_produto_por_codigo():
    codigo = request.args.get('codigo', '').strip()

    if not codigo:
        return jsonify({"error": "Parâmetro 'codigo' não informado"}), 400

    conn = conectar()
    cursor = conn.cursor()

    query = """
        SELECT Codigo, InformeProduto, Fornecedor, TipoFornecedor, Quantidade
        FROM CadastroProdutoServico
        WHERE Codigo = ?
    """
    cursor.execute(query, (codigo,))
    linha = cursor.fetchone()
    conn.close()

    if linha:
        produto = {
            "Codigo": linha[0],
            "InformeProduto": linha[1],
            "Fornecedor": linha[2],
            "TipoFornecedor": linha[3],
            "Quantidade": linha[4]
        }
        return jsonify([produto])
    else:
        return jsonify([])  # retorna lista vazia se não achar

@app.route("/CadastroProdutoServico/buscarPorNome", methods=["GET"])
def buscar_usuario_por_nome():
    nome = request.args.get('nome', '').strip()

    conn = conectar()
    cursor = conn.cursor()

    query = """
        SELECT IDCadastroUsuario, NomeUsuario, SenhaUsuario, SetorUsuario
        FROM CadastroUsuario
        WHERE LOWER(NomeUsuario) LIKE LOWER(?)
    """
    cursor.execute(query, ('%' + nome + '%',))

    dados = [
        {"id": row[0], "NomeUsuario": row[1], "SenhaUsuario": row[2], "SetorUsuario": row[3]}
        for row in cursor.fetchall()
    ]

    conn.close()
    return jsonify(dados)
