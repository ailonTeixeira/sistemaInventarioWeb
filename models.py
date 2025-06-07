import sqlite3

DATABASE = 'database.db'

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    conn = sqlite3.connect(DATABASE)
    # Retorna as linhas como dicionários em vez de tuplas
    conn.row_factory = sqlite3.Row
    return conn

def resetar_estoque():
    """
    Função para limpar e recriar o banco de dados durante os testes.
    Importante: Esta função não deve ser usada em produção.
    """
    conn = get_db_connection()
    with open('schema.sql') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

def criar_produto(dados):
    """Cria um novo produto no banco de dados."""
    # Validações de negócio (permanecem as mesmas)
    campos_obrigatorios = ["nome", "categoria", "preco_unitario", "quantidade_inicial"]
    for campo in campos_obrigatorios:
        if campo not in dados:
            return None, f"Campo '{campo}' é obrigatório."
            
    nome = dados["nome"]
    categoria = dados["categoria"]
    preco = dados["preco_unitario"]
    qtd = dados["quantidade_inicial"]
    
    if not isinstance(nome, str) or not nome.strip():
        return None, "O campo 'nome' não pode ser vazio."
    if not isinstance(categoria, str) or not categoria.strip():
        return None, "O campo 'categoria' não pode ser vazio."
    if not isinstance(preco, (int, float)) or preco <= 0:
        return None, "O preço unitário deve ser um número positivo."
    if not isinstance(qtd, int) or qtd < 0:
        return None, "A quantidade inicial deve ser um número inteiro maior ou igual a zero."

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO produtos (nome, categoria, preco_unitario, quantidade) VALUES (?, ?, ?, ?)',
            (nome.strip(), categoria.strip(), preco, qtd)
        )
        produto_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Retorna o produto recém-criado
        return obter_produto_por_id(produto_id), None
    except sqlite3.Error as e:
        return None, f"Erro no banco de dados: {e}"

def listar_produtos(nome=None, categoria=None):
    """Lista produtos do banco de dados, com suporte a filtros."""
    conn = get_db_connection()
    query = 'SELECT * FROM produtos'
    params = []
    
    conditions = []
    if nome:
        conditions.append('nome LIKE ?')
        params.append(f'%{nome}%')
    if categoria:
        conditions.append('categoria LIKE ?')
        params.append(f'%{categoria}%')
        
    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)

    produtos_raw = conn.execute(query, params).fetchall()
    conn.close()
    
    # Converte os objetos Row para dicionários
    produtos = [dict(p) for p in produtos_raw]
    return produtos

def obter_produto_por_id(produto_id):
    """Retorna um único produto pelo seu ID do banco de dados."""
    conn = get_db_connection()
    produto_raw = conn.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,)).fetchone()
    conn.close()
    if produto_raw is None:
        return None
    return dict(produto_raw)

def atualizar_produto(produto_id, dados):
    """Atualiza os dados de um produto no banco de dados."""
    produto_atual = obter_produto_por_id(produto_id)
    if not produto_atual:
        return None, "Produto não encontrado."
    
    # Prepara os campos para atualização
    campos_para_atualizar = {}
    if "nome" in dados: campos_para_atualizar['nome'] = dados['nome'].strip()
    if "categoria" in dados: campos_para_atualizar['categoria'] = dados['categoria'].strip()
    if "preco_unitario" in dados: campos_para_atualizar['preco_unitario'] = dados['preco_unitario']

    if not campos_para_atualizar:
        return produto_atual, None # Nenhum dado para atualizar

    set_clause = ', '.join([f'{campo} = ?' for campo in campos_para_atualizar])
    params = list(campos_para_atualizar.values())
    params.append(produto_id)

    conn = get_db_connection()
    conn.execute(f'UPDATE produtos SET {set_clause} WHERE id = ?', params)
    conn.commit()
    conn.close()

    return obter_produto_por_id(produto_id), None

def remover_produto(produto_id):
    """Remove um produto do banco de dados."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM produtos WHERE id = ?', (produto_id,))
    conn.commit()
    removido = cursor.rowcount > 0
    conn.close()
    return removido

def registrar_operacao_estoque(produto_id, tipo, quantidade):
    """Registra entrada ou saída de estoque no banco de dados."""
    produto = obter_produto_por_id(produto_id)
    if not produto:
        return None, "Produto não encontrado."

    if not isinstance(quantidade, int) or quantidade <= 0:
        return None, "A quantidade deve ser um número inteiro positivo."
        
    nova_quantidade = produto["quantidade"]
    if tipo == "entrada":
        nova_quantidade += quantidade
    elif tipo == "saida":
        if produto["quantidade"] < quantidade:
            return None, "Estoque insuficiente para a saída."
        nova_quantidade -= quantidade
    else:
        return None, "Tipo de operação inválida. Use 'entrada' ou 'saida'."

    conn = get_db_connection()
    conn.execute('UPDATE produtos SET quantidade = ? WHERE id = ?', (nova_quantidade, produto_id))
    conn.commit()
    conn.close()
    
    return obter_produto_por_id(produto_id), None