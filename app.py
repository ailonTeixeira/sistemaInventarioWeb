from flask import Flask
from routes import inventario_routes
from web_routes import web_routes # <-- 1. Importar as novas rotas

def create_app():
    """Cria e configura uma instância da aplicação Flask."""
    app = Flask(__name__)
    
    # Chave secreta necessária para usar 'flash messages'
    app.config['SECRET_KEY'] = 'uma-chave-secreta-qualquer-para-o-projeto'

    app.register_blueprint(inventario_routes) # Blueprint da API
    app.register_blueprint(web_routes) # <-- 2. Registrar o blueprint da interface web
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)