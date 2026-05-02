from flask import Flask
from config import Config
from app.extensions import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes.main import main_bp
    from app.routes.product import product_bp
    from app.routes.checkout import checkout_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(checkout_bp)
    app.register_blueprint(admin_bp)

    register_commands(app)

    return app


def register_commands(app):
    @app.cli.command("init-db")
    def init_db_command():
        from app.seed import seed_products

        db.create_all()
        seed_products()
        print("Database initialized.")
