from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'sua_chave_secreta_aqui_123!@#'  # Apenas para exemplo, mudar a abordagem de secret_key.
    # Importa e registra as rotas
    from app.routes import main
    app.register_blueprint(main)

    return app
