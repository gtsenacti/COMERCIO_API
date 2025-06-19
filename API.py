from CONECTAR.funcaoConectar import conectar
from flask import Flask, jsonify


app = Flask(__name__)

#Tabela cadastro usuario
@app.route("/CadastroUsuario", methods=["GET"])
def listar_Cadastros():
    conn = conectar()
    #conn.execute("PRAGMA foreign_keys = ON") #ativa as chaves estrangeiras das tabelas (pois, não é ativado por padrão)
    cursor = conn.cursor()
    cursor.execute("SELECT IDCadastroUsuario, NomeUsuario, SenhaUsuario, SetorUsuario FROM CadastroUsuario")
    dados = [
        {"id": row[0], "NomeUsuario": row[1], "SenhaUsuario": row[2], "SetorUsuario": row[3]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(dados)


#Tabela cadastro produto 
@app.route("/CadastroProduto", methods=["GET"])
def listar_CadastrosProdutos():
    conn = conectar()
    #conn.execute("PRAGMA foreign_keys = ON") #ativa as chaves estrangeiras das tabelas (pois, não é ativado por padrão)
    cursor = conn.cursor()
    cursor.execute("SELECT IDCadastroProduto, Produto, Fornecedor, cnpj FROM CadastroProduto")
    dados = [
        {"id": row[0], "NomeProduto": row[1], "NomeFornecedor": row[2], "CNPJFornecedor": row[3]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(dados)



if __name__ == "__main__":
    app.run(debug=True)

