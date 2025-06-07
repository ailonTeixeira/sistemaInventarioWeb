from flask import Blueprint, jsonify, request
from models import (
    criar_produto, listar_produtos, obter_produto_por_id,
    atualizar_produto, remover_produto, registrar_operacao_estoque
)

inventario_routes = Blueprint("inventario", __name__)

# Rota para criar um novo produto (POST /produtos)
@inventario_routes.route("/produtos", methods=["POST"])
def rota_criar_produto():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Corpo da requisição não pode ser vazio"}), 400
        
    produto, erro = criar_produto(dados)
    if erro:
        return jsonify({"erro": erro}), 400  # Bad Request
        
    return jsonify(produto), 201

# Rota para listar produtos (GET /produtos) com filtros
@inventario_routes.route("/produtos", methods=["GET"])
def rota_listar_produtos():
    nome = request.args.get('nome')
    categoria = request.args.get('categoria')
    
    produtos = listar_produtos(nome=nome, categoria=categoria)
    return jsonify(produtos), 200

# Rota para obter um produto por ID (GET /produtos/<id>)
@inventario_routes.route("/produtos/<int:produto_id>", methods=["GET"])
def rota_obter_produto(produto_id):
    produto = obter_produto_por_id(produto_id)
    if produto:
        return jsonify(produto), 200
    return jsonify({"erro": "Produto não encontrado"}), 404

# Rota para atualizar um produto (PUT /produtos/<id>)
@inventario_routes.route("/produtos/<int:produto_id>", methods=["PUT"])
def rota_atualizar_produto(produto_id):
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Corpo da requisição não pode ser vazio"}), 400
        
    produto, erro = atualizar_produto(produto_id, dados)
    if erro == "Produto não encontrado.":
        return jsonify({"erro": erro}), 404
    if erro:
        return jsonify({"erro": erro}), 400

    return jsonify(produto), 200

# Rota para remover um produto (DELETE /produtos/<id>)
@inventario_routes.route("/produtos/<int:produto_id>", methods=["DELETE"])
def rota_remover_produto(produto_id):
    if remover_produto(produto_id):
        return '', 204  # No Content
    return jsonify({"erro": "Produto não encontrado"}), 404

# Rota para operações de estoque (POST /produtos/<id>/estoque)
@inventario_routes.route("/produtos/<int:produto_id>/estoque", methods=["POST"])
def rota_operacao_estoque(produto_id):
    dados = request.get_json()
    if not dados or "tipo" not in dados or "quantidade" not in dados:
        return jsonify({"erro": "Campos 'tipo' e 'quantidade' são obrigatórios."}), 400

    tipo = dados["tipo"]
    quantidade = dados["quantidade"]
    
    produto, erro = registrar_operacao_estoque(produto_id, tipo, quantidade)

    if erro == "Produto não encontrado.":
        return jsonify({"erro": erro}), 404
    if erro:
        return jsonify({"erro": erro}), 400
    
    return jsonify(produto), 200