# 🎓 Sistema de Gerenciamento de Inventário

Uma aplicação web completa e segura para gerenciamento de inventário, desenvolvida com Python e Flask. O sistema possui persistência de dados com **SQLite**, **autenticação de usuário** e uma **API REST** para integrações.

## ✅ Funcionalidades Principais

- **Persistência de Dados:** Utiliza **SQLite** para que os dados sejam salvos permanentemente.
- **Autenticação Segura:** Uma tela de login protege o acesso ao sistema, garantindo que apenas usuários autorizados possam gerenciar o inventário.
- **Interface Web Completa:** Uma interface visual intuitiva para realizar todas as operações (CRUD de produtos e controle de estoque).
- **API REST Robusta:** Endpoints para todas as operações, permitindo integrações com outros sistemas de forma automatizada.
- **Testes Automatizados:** Cobertura de testes com `pytest` para garantir a confiabilidade da lógica de negócio e da API.

## 🛠️ Requisitos Técnicos

- Python 3.8+
- Flask
- Pytest
- SQLite

## 🚀 Como Executar (Modo Automatizado com `run.sh`)

Este método é recomendado para ambientes macOS e Linux.

1.  Dê permissão de execução ao script:
    ```bash
    chmod +x run.sh
    ```
2.  Execute o script:
    ```bash
    ./run.sh
    ```
O script irá automaticamente:
- Criar o ambiente virtual.
- Instalar as dependências.
- **Criar o banco de dados `database.db` (se não existir).**
- Rodar os testes.
- Iniciar a aplicação.

## ⚙️ Como Executar (Modo Manual)

### 1. Preparação do Ambiente

Clone este repositório e navegue até a pasta do projeto.

```bash
git clone https://github.com/ailonTeixeira/sistemaInventarioWeb
cd sistema-inventarioWeb
```

Crie e ative um ambiente virtual:

```bash
# Para Windows
python -m venv venv
.\venv\Scripts\activate

# Para macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

### 2. Inicialização do Banco de Dados

**Execute este comando apenas uma vez**, antes de rodar a aplicação pela primeira vez.

```bash
python init_db.py
```
Isso criará o arquivo `database.db`, que armazenará todos os dados.

### 3. Executando a Aplicação

Inicie o servidor Flask:

```bash
python app.py
```

## 🔐 Acesso ao Sistema

1.  Abra seu navegador e acesse **[http://127.0.0.1:5000](http://127.0.0.1:5000)**.
2.  Você será redirecionado para a tela de login. Use as seguintes credenciais para acessar:
    - **Usuário:** `admin`
    - **Senha:** `1234`

Após o login, você terá acesso total à interface de gerenciamento de inventário.

---

### 🤖 API REST (Para Integrações)


A API REST continua totalmente funcional. Note que os endpoints da API **não estão protegidos** pela autenticação da sessão web, permitindo integrações por outros sistemas (em um projeto real, a API teria sua própria segurança, como tokens).

# 📖 Documentação da API

### `POST /produtos`
Cria um novo produto.

**Exemplo com cURL:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{
    "nome": "Mouse sem Fio",
    "categoria": "Periféricos",
    "preco_unitario": 89.90,
    "quantidade_inicial": 50
}' http://127.0.0.1:5000/produtos
```

### `GET /produtos`
Lista todos os produtos. Suporta filtros via query string.

**Exemplos:**
```bash
# Listar todos
curl http://127.0.0.1:5000/produtos

# Filtrar por nome
curl "http://127.0.0.1:5000/produtos?nome=mouse"

# Filtrar por categoria
curl "http://127.0.0.1:5000/produtos?categoria=Periféricos"
```

### `GET /produtos/<id>`
Consulta um produto específico pelo ID.

```bash
curl http://127.0.0.1:5000/produtos/1
```

### `PUT /produtos/<id>`
Atualiza os dados de um produto.

```bash
curl -X PUT -H "Content-Type: application/json" -d '{
    "preco_unitario": 95.00
}' http://127.0.0.1:5000/produtos/1
```

### `DELETE /produtos/<id>`
Remove um produto do inventário.

```bash
curl -X DELETE http://127.0.0.1:5000/produtos/1
```

### `POST /produtos/<id>/estoque`
Registra uma operação de entrada ou saída no estoque.

**Exemplo (Entrada):**
```bash
curl -X POST -H "Content-Type: application/json" -d '{
    "tipo": "entrada",
    "quantidade": 10
}' http://127.0.0.1:5000/produtos/1/estoque
```

**Exemplo (Saída):**
```bash
curl -X POST -H "Content-Type: application/json" -d '{
    "tipo": "saida",
    "quantidade": 5
}' http://127.0.0.1:5000/produtos/1/estoque
```
