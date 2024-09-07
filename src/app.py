from flask import Flask
from config import Config
from search import search_bp
from upload_api import upload_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(search_bp)
    app.register_blueprint(upload_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
