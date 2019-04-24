# -*- encoding: utf-8 -*-

import json

from flask import render_template
from flask import Blueprint

from flaskmongo.db import mongo
from flaskmongo.utils import TemplateValues


bp = Blueprint('about', __name__, url_prefix='/about')


@bp.route("/", methods=('GET',))
def index():
    """ Página do "sobre". """
    t_values = TemplateValues()
    t_values.set('nav', 'about')
    t_values.set('title', 'Sobre')
    return render_template('about.html', **t_values.values)