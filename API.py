from CONECTAR.funcaoConectar import conectar
from flask import Flask, jsonify


app = Flask(__name__)

#rota tabela cadastro usuatio#
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
#rota tabela CadastroProdutoServico#
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
#rota tabela FornecedorProduto#
@app.route("/FornecedorProduto", methods=["GET"])
def listar_FornecedorProduto():
    conn = conectar()
    #conn.execute("PRAGMA foreign_keys = ON") #ativa as chaves estrangeiras das tabelas (pois, não é ativado por padrão)
    cursor = conn.cursor()
    cursor.execute("SELECT Cnpj, CodBarraFornecedor, InformeProdutoForn, NomeFornecedor,EndFornecedor FROM FornecedorProduto")
    dados = [
        {"Cnpj": row[0], "CodBarraFornecedor": row[1], "InformeProdutoForn": row[2], "NomeFornecedor": row[3], "EndFornecedor": row[4]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(dados)

#---------------------------------#
if __name__ == "__main__":
    app.run(debug=True)

