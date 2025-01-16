from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db_user = SQLAlchemy()
from api import api_blueprint
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db_user.init_app(app)
    app.register_blueprint(api_blueprint, url_prefix='/api')
    with app.app_context():
        db_user.create_all()
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
