# -*- encoding: utf-8 -*-

import json

from bson.objectid import ObjectId
from flask import render_template
from flask import render_template_string
from flask import jsonify
from flask import request
from flask import Blueprint

from flaskmongo.db import mongo
from flaskmongo.utils import TemplateValues
from flaskmongo.utils import normalize_text


bp = Blueprint('flights', __name__, url_prefix='/flights')


@bp.route("/<flight_id>/save", methods=['POST'])
def flights_save(flight_id):
    """ Salva as alterações de um voo. """
    json_ = request.form['json']
    flight_to_up = json.loads(json_)
    result = {'ok': False, 'error': None, 'flight': None}
    if flight_to_up:
        res = mongo.db.flights.update_one({'_id': ObjectId(flight_id)}, {'$set': flight_to_up})
        if res.matched_count > 0:
            flight = mongo.db.flights.find_one({'_id': ObjectId(flight_id)})
            result['ok'] = True
            result['flight'] = flight
        else:
            result['error'] = 'O voo %s não foi encontrado para ser alterado.' % (flight_id)
    else:
        result['error'] = 'Não foram enviados parâmetros para serem alterados.'
    return jsonify(result)


@bp.route("/search", methods=['GET'])
def flights_search():
    """ Busca por voos.
    Pode buscar pelos IDs dos aeroportos ou pelos nomes. """
    from_ = request.args.get('from', '')
    to_ = request.args.get('to', '')
    from_id = request.args.get('from_id', '')
    to_id = request.args.get('to_id', '')
    data = {'html': ''}

    query_params = {}

    if from_id and from_:
        query_params['from_airport._id'] = from_id
    elif from_:
        from_ = normalize_text(from_)
        query_params['from_airport.searchable'] = {'$regex': '^%s.*$' % (from_) , '$options': 's'}

    if to_id and to_:
        # Deve verificar o "to_" também, pois se o campo ficar vazio o JS não limpa o ID e pode conter um ID de uma busca anterior válida.
        query_params['to_airport._id'] = to_id
    elif to_:
        to_ = normalize_text(to_)
        query_params['to_airport.searchable'] = {'$regex': '^%s.*$' % (to_) , '$options': 's'}

    if query_params:
        query_params['available'] = True
        # Consulta no mongo.
        flights = mongo.db.flights.find(query_params)
        flights = list(flights)
    else:
        flights = []

    t_values = TemplateValues()
    t_values.set('flights', flights)
    data['html'] = render_template('flights_results.html', **t_values.values)
    return jsonify(data)


@bp.route("/check", methods=['GET'])
def flights_check():
    """ Verifica e retorna sugestões de voos.

    Retorna um JSON neste formato:
    {
        "query": "Unit",
        "suggestions": [
            {"value": "Cidade1 - Aeroporto1", "data": "ID_DO_AEROPORTO1"},
            {"value": "Cidade2 - Aeroporto2", "data": "ID_DO_AEROPORTO2"},
            ...
        ]
    }
    
    * Este é o formato aceito pelo plugin JS que faz o efeito de autocomplete.

    """
    direction = request.args.get('direction', 'from')
    query = request.args.get('query', '')
    suggestions = []
    data = {'query': 'Unit', 'suggestions': suggestions}

    query = normalize_text(query)
    from_id = None

    if not query:
        return jsonify(data)

    if direction == 'to':
        from_id = request.args.get('from_id', '')
        if not from_id:
            return jsonify(data)

    if direction == 'from':
        pipelines = [
            {'$match': {'from_airport.searchable': {'$regex': '^%s.*$' % (query) , '$options': 's'}, 'available': True}},
            {'$group': {'_id': '$from_airport.searchable'}},
            {'$sort' : {'from_airport.searchable': 1}},
            {'$limit': 10},
        ]
    else:
        pipelines = [
            {
                '$match': {
                    'from_airport._id': from_id,
                    'to_airport.searchable': {'$regex': '^%s.*$' % (query) , '$options': 's'},
                    'available': True
                }
            },
            {'$group': {'_id': '$to_airport.searchable'}},
            {'$sort' : {'to_airport.searchable': 1}},
            {'$limit': 10},
        ]
    flights = mongo.db.flights.aggregate(pipelines)
    aiports_ids = [f['_id'].split(';')[-1] for f in flights]
    if aiports_ids:
        airports = mongo.db.airports.find({'_id': {'$in': aiports_ids}})
        for a in airports:
            suggestions.append({
                'data': a['_id'],
                'value': '%s - %s' %(a['city'], a['name'])  # valor apresentado como sugestão
            })
    
    return jsonify(data)