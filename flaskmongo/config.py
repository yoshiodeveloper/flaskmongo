# -*- encoding: utf-8 -*-

import os


# Nome da empresa fictícia.
COMPANY_NAME = 'TheCompanyName'

# Valores padrões que são enviados a todos os templates.
DEFAULT_TEMPLATE_VALUES = {
    'COMPANY_NAME': COMPANY_NAME
}

# Nome do banco de dados no mongo.
MONGO_DB = os.getenv('MONGO_DB') or 'flaskmongo'

# URL de conexão com o mongo.
MONGO_URI = os.getenv('MONGO_URI') or 'mongodb://127.0.0.1:27017/%s' % MONGO_DB

try:
    # Sobrescreve as configurações pelo valore em "flaskmongo.instance.config".
    from flaskmongo.local_config import *
except importError:
    pass