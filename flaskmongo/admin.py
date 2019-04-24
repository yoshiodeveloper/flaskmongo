# -*- encoding: utf-8 -*-

import json

from flask import render_template
from flask import Blueprint

from flaskmongo.db import mongo
from flaskmongo.utils import TemplateValues


bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route("/flights", methods=('GET',))
def flights():
    """ Página principal da administração. """
    t_values = TemplateValues()
    t_values.set('nav', 'admin')
    t_values.set('title', 'Administração')
    flights = mongo.db.flights.find().sort([('from_airport.searchable', 1)])
    t_values.set('flights', flights)
    return render_template('admin_flights.html', **t_values.values)