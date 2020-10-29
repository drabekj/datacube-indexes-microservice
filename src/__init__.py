from flask import Flask

from .config import config_by_name


def factory_build_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    return app
