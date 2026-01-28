"""FlipBook SaaS - Application Flask"""

from flask import Flask
from config import config, init_directories, MAX_FILE_SIZE_MB

from routes.main import main_bp
from routes.upload import upload_bp
from routes.viewer import viewer_bp
from routes.editor import editor_bp


def create_app():
    """Factory pattern pour créer l'application"""
    app = Flask(__name__)
    app.config.from_object(config)
    
    init_directories()
    
    # Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(viewer_bp)
    app.register_blueprint(editor_bp)
    
    # Erreurs globales
    @app.errorhandler(404)
    def not_found(e):
        return {"error": "Page non trouvée"}, 404
    
    @app.errorhandler(413)
    def file_too_large(e):
        return {"error": f"Fichier trop volumineux (max {MAX_FILE_SIZE_MB} MB)"}, 413
    
    @app.errorhandler(500)
    def server_error(e):
        return {"error": "Erreur serveur"}, 500
    
    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
