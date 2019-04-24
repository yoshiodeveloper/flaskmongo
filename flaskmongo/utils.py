# -*- encoding: utf-8 -*-

import unicodedata

from bson.objectid import ObjectId
from flask.json import JSONEncoder

from flaskmongo.config import DEFAULT_TEMPLATE_VALUES


class MongoJSONEncoder(JSONEncoder):
    """ Classe utilizada para codificar os objetos em JSON. É utilizado pela função jsonify do Flask.
    Em especial é transformados os IDs do tipo ObjectId do Mongo em string.
    """

    def default(self, o):
        if isinstance(o, ObjectId):
            # Se o tipo for um ObjectId então converte para a sua forma em string.
            return str(o)
        else:
            # Se for de outros tipos utiliza o método "defaul" do JSONEncoder.
            return super().default(o)


class TemplateValues(object):
    """ Classe utilizada para gerar os valores enviados aos templates.
    Em especiais são adicionados automaticamente os valores de DEFAULT_REQUEST_VALUES. 
    """
    def __init__(self):
        self.values = DEFAULT_TEMPLATE_VALUES.copy()

    def set(self, k, v):
        """ Adicionar/altera um valor `v` da chave `k` no dicionário interno `values`. """
        self.values[k] = v

    def get(self, k, default=None):
        """ Retorna o valor da chave `k` do dicionário interno `values`.
        Pode-se indicar um valor padrão em `default` que é retornado caso a chave não exista.
        """
        return self.values.get(k, default)


def normalize_text(text):
    """ Normaliza um texto para otimizar as buscas.
    - Remove os acentos.
    - Remove os traços.
    - Remove os espaços duplos.
    - Remove os espaços das extremidades.
    - Altera o texto para minúsculo.
    
    Exemplo:
    
    >>> print(normalize_text('São Paulo -     Congonhas'))
    sao paulo congonhas
    >>>

    :param text: Texto que deve ser normalizado.
    :returns: Texto normalizado.
    """
    if not text:
        return text
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ASCII', 'ignore')
    text = text.decode('utf-8')
    text = text.replace('-', ' ')
    while '  ' in text:
        text = text.replace('  ', ' ')
    text = text.strip().lower()
    return text