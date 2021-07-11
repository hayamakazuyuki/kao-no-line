from flask import Flask

from .extentions import admin, db


def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    db.init_app(app)
    admin.init_app(app)

    from .user.views import user
    from .main.views import main
    app.register_blueprint(main)
    app.register_blueprint(user)

    return app
