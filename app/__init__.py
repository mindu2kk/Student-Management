from flask import Flask
from .config import Config
from .extensions import db, migrate
from .routes import api_bp
from .ui import ui_bp


def create_app(config_class: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(ui_bp)

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    return app


