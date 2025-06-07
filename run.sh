# Script para configurar e executar o Sistema de Gerenciamento de Inventário

echo "====================================================="
echo "🚀 Iniciando setup do Sistema de Inventário..."
echo "====================================================="

# Verifica se o python3 está instalado
if ! command -v python3 &> /dev/null
then
    echo "❌ Erro: python3 não encontrado. Por favor, instale o Python 3."
    exit 1
fi

# 1. Criação do ambiente virtual
echo "-> 1/5: Criando ambiente virtual na pasta 'venv'..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "❌ Falha ao criar o ambiente virtual."
    exit 1
fi

# 2. Ativação do ambiente virtual
echo "-> 2/5: Ativando o ambiente virtual..."
source venv/bin/activate

# 3. Instalação das dependências
echo "-> 3/5: Instalando as dependências do requirements.txt..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Falha ao instalar as dependências."
    exit 1
fi

# 4. Inicialização do Banco de Dados
echo "-> 4/5: Verificando e inicializando o banco de dados..."
if [ ! -f database.db ]; then
    echo "   Arquivo 'database.db' não encontrado. Criando..."
    python init_db.py
else
    echo "   Banco de dados já existe. Pulando a criação."
fi

echo "✅ Setup concluído com sucesso!"
echo ""
echo "====================================================="
echo "🧪 Executando testes automatizados..."
echo "====================================================="

# 5. Execução dos testes
pytest
if [ $? -ne 0 ]; then
    echo "⚠️ Atenção: Um ou mais testes falharam. Verifique o output acima."
    # exit 1 
fi

echo ""
echo "====================================================="
echo "🔥 Iniciando a aplicação Flask..."
echo "A API estará disponível em: http://127.0.0.1:5000"
echo "Pressione CTRL+C para parar o servidor."
echo "====================================================="
python app.py