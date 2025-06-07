# web_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps # Importa wraps para criar o decorator
from models import (
    listar_produtos, obter_produto_por_id, criar_produto, 
    atualizar_produto, remover_produto, registrar_operacao_estoque
)

web_routes = Blueprint('web', __name__, template_folder='templates')

# --- Credenciais fixas para o exemplo ---
USUARIO_VALIDO = "admin"
SENHA_VALIDA = "1234"

# --- Decorator para proteger rotas ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash("Por favor, faça login para acessar esta página.", "warning")
            return redirect(url_for('web.login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Novas rotas de autenticação ---
@web_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")
        if usuario == USUARIO_VALIDO and senha == SENHA_VALIDA:
            session['logged_in'] = True
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("web.index"))
        else:
            flash("Usuário ou senha inválidos.", "danger")
    return render_template("login.html")

@web_routes.route("/logout")
def logout():
    session.pop('logged_in', None)
    flash("Você foi desconectado.", "info")
    return redirect(url_for('web.login'))

# --- Protegendo as rotas existentes ---
@web_routes.route("/")
@login_required
def index():
    # ... (código existente sem alteração)
    produtos = listar_produtos()
    return render_template("index.html", produtos=produtos)

@web_routes.route("/produto/novo", methods=["GET", "POST"])
@login_required
def novo_produto():
    # ... (código existente sem alteração)
    if request.method == "POST":
        dados = {
            "nome": request.form.get("nome"),
            "categoria": request.form.get("categoria"),
            "preco_unitario": float(request.form.get("preco_unitario")),
            "quantidade_inicial": int(request.form.get("quantidade_inicial"))
        }
        produto, erro = criar_produto(dados)
        if erro:
            flash(f"Erro ao criar produto: {erro}", "danger")
        else:
            flash(f"Produto '{produto['nome']}' criado com sucesso!", "success")
        return redirect(url_for("web.index"))

    return render_template("produto_form.html", titulo="Novo Produto", produto=None)


# ... (Adicione o decorator @login_required em TODAS as outras rotas web) ...
@web_routes.route("/produto/<int:produto_id>")
@login_required
def detalhe_produto(produto_id):
    """Página de detalhes de um produto."""
    produto = obter_produto_por_id(produto_id)
    if not produto:
        flash("Produto não encontrado.", "warning")
        return redirect(url_for("web.index"))
    return render_template("produto_detalhe.html", produto=produto)

@web_routes.route("/produto/<int:produto_id>/editar", methods=["GET", "POST"])
@login_required
def editar_produto(produto_id):
    """Página para editar um produto existente."""
    produto = obter_produto_por_id(produto_id)
    if not produto:
        flash("Produto não encontrado.", "warning")
        return redirect(url_for("web.index"))

    if request.method == "POST":
        dados = {
            "nome": request.form.get("nome"),
            "categoria": request.form.get("categoria"),
            "preco_unitario": float(request.form.get("preco_unitario"))
        }
        produto_atualizado, erro = atualizar_produto(produto_id, dados)
        if erro:
            flash(f"Erro ao atualizar produto: {erro}", "danger")
        else:
            flash(f"Produto '{produto_atualizado['nome']}' atualizado com sucesso!", "success")
        return redirect(url_for("web.detalhe_produto", produto_id=produto_id))

    return render_template("produto_form.html", titulo="Editar Produto", produto=produto)   
@web_routes.route("/produto/<int:produto_id>/remover", methods=["POST"])
@login_required
def remover_produto_web(produto_id):
    """Rota para remover um produto."""
    produto = obter_produto_por_id(produto_id)
    if remover_produto(produto_id):
        flash(f"Produto '{produto['nome']}' removido com sucesso!", "success")
    else:
        flash("Erro ao remover o produto.", "danger")
    return redirect(url_for("web.index"))

@web_routes.route("/produto/<int:produto_id>/estoque", methods=["POST"])
@login_required
def operar_estoque_web(produto_id):
    """Rota para registrar entrada ou saída de estoque."""
    tipo = request.form.get("tipo")
    try:
        quantidade = int(request.form.get("quantidade"))
        produto, erro = registrar_operacao_estoque(produto_id, tipo, quantidade)
        if erro:
            flash(f"Erro na operação de estoque: {erro}", "danger")
        else:
            flash(f"Operação de '{tipo}' de {quantidade} unidade(s) registrada com sucesso!", "success")
    except (ValueError, TypeError):
        flash("Quantidade inválida.", "danger")
        
    return redirect(url_for("web.detalhe_produto", produto_id=produto_id))