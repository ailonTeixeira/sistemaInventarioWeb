# tests/test_api.py

import pytest
import json
from app import create_app
from models import resetar_estoque

@pytest.fixture
def client():
    """Cria um cliente de teste para a aplicação Flask."""
    app = create_app()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        # Reseta o estado do estoque antes de cada teste
        resetar_estoque()
        yield client

# === Testes de Criação de Produto (POST /produtos) ===

def test_criar_produto_sucesso(client):
    """Testa a criação bem-sucedida de um produto."""
    dados = {
        "nome": "Notebook Gamer",
        "categoria": "Eletrônicos",
        "preco_unitario": 5500.00,
        "quantidade_inicial": 10
    }
    response = client.post('/produtos', data=json.dumps(dados), content_type='application/json')
    assert response.status_code == 201
    produto = response.get_json()
    assert produto['nome'] == "Notebook Gamer"
    assert produto['id'] == 1

def test_criar_produto_dados_invalidos(client):
    """Testa a criação de produto com dados inválidos (preço negativo)."""
    dados = {
        "nome": "Mousepad",
        "categoria": "Acessórios",
        "preco_unitario": -20.00,
        "quantidade_inicial": 50
    }
    response = client.post('/produtos', data=json.dumps(dados), content_type='application/json')
    assert response.status_code == 400
    assert "erro" in response.get_json()

def test_criar_produto_campo_faltando(client):
    """Testa a criação de produto com um campo obrigatório faltando."""
    dados = {"nome": "Teclado Mecânico", "preco_unitario": 350.00}
    response = client.post('/produtos', data=json.dumps(dados), content_type='application/json')
    assert response.status_code == 400
    assert "Campo 'categoria' é obrigatório" in response.get_json()['erro']

# === Testes de Listagem de Produtos (GET /produtos) ===

def test_listar_produtos_vazio(client):
    """Testa a listagem quando não há produtos."""
    response = client.get('/produtos')
    assert response.status_code == 200
    assert response.get_json() == []

def test_listar_produtos_com_itens(client):
    """Testa a listagem com produtos já cadastrados."""
    # Adiciona um produto primeiro
    client.post('/produtos', data=json.dumps({"nome": "Monitor 24 polegadas", "categoria": "Monitores", "preco_unitario": 1200, "quantidade_inicial": 5}), content_type='application/json')
    
    response = client.get('/produtos')
    assert response.status_code == 200
    produtos = response.get_json()
    assert len(produtos) == 1
    assert produtos[0]['nome'] == "Monitor 24 polegadas"

def test_listar_produtos_com_filtro(client):
    """Testa a listagem com filtro por nome e categoria."""
    client.post('/produtos', data=json.dumps({"nome": "Cadeira Gamer", "categoria": "Móveis", "preco_unitario": 950, "quantidade_inicial": 15}), content_type='application/json')
    client.post('/produtos', data=json.dumps({"nome": "Mesa Gamer", "categoria": "Móveis", "preco_unitario": 800, "quantidade_inicial": 10}), content_type='application/json')
    
    # Filtro por nome
    response = client.get('/produtos?nome=cadeira')
    assert response.status_code == 200
    assert len(response.get_json()) == 1
    assert response.get_json()[0]['nome'] == "Cadeira Gamer"

    # Filtro por categoria
    response = client.get('/produtos?categoria=Móveis')
    assert response.status_code == 200
    assert len(response.get_json()) == 2

# === Testes de Consulta, Atualização e Remoção ===

def test_obter_produto_por_id(client):
    """Testa a consulta de um produto específico."""
    res_post = client.post('/produtos', data=json.dumps({"nome": "Webcam HD", "categoria": "Periféricos", "preco_unitario": 250, "quantidade_inicial": 30}), content_type='application/json')
    produto_id = res_post.get_json()['id']

    response = client.get(f'/produtos/{produto_id}')
    assert response.status_code == 200
    assert response.get_json()['nome'] == "Webcam HD"

def test_obter_produto_nao_existente(client):
    """Testa a consulta de um produto que não existe."""
    response = client.get('/produtos/999')
    assert response.status_code == 404

def test_atualizar_produto(client):
    """Testa a atualização de um produto."""
    res_post = client.post('/produtos', data=json.dumps({"nome": "Fone de Ouvido", "categoria": "Audio", "preco_unitario": 150, "quantidade_inicial": 25}), content_type='application/json')
    produto_id = res_post.get_json()['id']
    
    dados_atualizados = {"preco_unitario": 175.50, "nome": "Headset Gamer Pro"}
    response = client.put(f'/produtos/{produto_id}', data=json.dumps(dados_atualizados), content_type='application/json')
    assert response.status_code == 200
    produto_atualizado = response.get_json()
    assert produto_atualizado['preco_unitario'] == 175.50
    assert produto_atualizado['nome'] == "Headset Gamer Pro"

def test_remover_produto(client):
    """Testa a remoção de um produto."""
    res_post = client.post('/produtos', data=json.dumps({"nome": "Produto a ser removido", "categoria": "Geral", "preco_unitario": 10, "quantidade_inicial": 1}), content_type='application/json')
    produto_id = res_post.get_json()['id']

    response_delete = client.delete(f'/produtos/{produto_id}')
    assert response_delete.status_code == 204

    response_get = client.get(f'/produtos/{produto_id}')
    assert response_get.status_code == 404

# === Testes de Operações de Estoque ===

def test_entrada_estoque(client):
    """Testa a adição de itens ao estoque."""
    res_post = client.post('/produtos', data=json.dumps({"nome": "SSD 1TB", "categoria": "Armazenamento", "preco_unitario": 450, "quantidade_inicial": 5}), content_type='application/json')
    produto_id = res_post.get_json()['id']
    
    operacao = {"tipo": "entrada", "quantidade": 10}
    response = client.post(f'/produtos/{produto_id}/estoque', data=json.dumps(operacao), content_type='application/json')
    
    assert response.status_code == 200
    produto_atualizado = response.get_json()
    assert produto_atualizado['quantidade'] == 15 # 5 (inicial) + 10 (entrada)

def test_saida_estoque(client):
    """Testa a remoção de itens do estoque."""
    res_post = client.post('/produtos', data=json.dumps({"nome": "Memória RAM 16GB", "categoria": "Componentes", "preco_unitario": 300, "quantidade_inicial": 20}), content_type='application/json')
    produto_id = res_post.get_json()['id']
    
    operacao = {"tipo": "saida", "quantidade": 5}
    response = client.post(f'/produtos/{produto_id}/estoque', data=json.dumps(operacao), content_type='application/json')
    
    assert response.status_code == 200
    assert response.get_json()['quantidade'] == 15

def test_saida_estoque_insuficiente(client):
    """Testa a tentativa de saída com estoque insuficiente."""
    res_post = client.post('/produtos', data=json.dumps({"nome": "Placa de Vídeo", "categoria": "Componentes", "preco_unitario": 3000, "quantidade_inicial": 2}), content_type='application/json')
    produto_id = res_post.get_json()['id']
    
    operacao = {"tipo": "saida", "quantidade": 5} # Tenta tirar 5, mas só tem 2
    response = client.post(f'/produtos/{produto_id}/estoque', data=json.dumps(operacao), content_type='application/json')
    
    assert response.status_code == 400
    assert "Estoque insuficiente" in response.get_json()['erro']