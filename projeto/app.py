from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'sua_chave_secreta'
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'documentos') 
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    from projeto.rotas import documentos_bp    
    app.register_blueprint(documentos_bp)

    return app