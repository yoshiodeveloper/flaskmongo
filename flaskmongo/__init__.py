# -*- encoding: utf-8 -*-

from flask import Flask
from flask import render_template
from flask_pymongo import PyMongo


def create_app(config_filename=None):
    from flaskmongo.utils import MongoJSONEncoder
    from flaskmongo.utils import TemplateValues

    app = Flask(__name__)
    app.json_encoder = MongoJSONEncoder
    app.config.from_object('flaskmongo.config')

    from flaskmongo.db import mongo
    mongo.init_app(app)

    @app.route("/", methods=('GET',))
    def index():
        t_values = TemplateValues()
        t_values.set('nav', 'flights')
        t_values.set('title', 'Voos')
        return render_template('index.html', **t_values.values)

    from flaskmongo import admin
    from flaskmongo import flights
    from flaskmongo import about
    app.register_blueprint(admin.bp)
    app.register_blueprint(flights.bp)
    app.register_blueprint(about.bp)
    return app