from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from DataBase.config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Swagger(app)

    with app.app_context():
        from DataBase.routes.book_routes import bp as books_bp
        app.register_blueprint(books_bp)

        db.create_all()

    return app
