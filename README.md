# flaskmongo

Trabalho sobre MongoDB feito em Python e Flask.

## Instalação no Linux

> É necessário ter o Python 3, virtualenv e MongoDB instalados.

Crie um virtualenv.

```shell
$ virtualenv -p python3 venv
```

Ative o ambiente.

```shell
$ source venv/bin/activate
```

Instale as libs do Python no ambiente utilizando o arquivo "requirements.txt".

```shell
$ pip install -r requirements.txt
```

Crie a base de dados inicial. É necessário que o MongoDB esteja instalado e rodando em "127.0.0.1:27017".

```shell
$ python bin/createdb.py
```

## Execução

Para iniciar a aplicação defina a variável de ambiente FLASK_APP, FLASK_ENV e execute o `flask run`.

```shell
export PYTHONPATH=$PYTHONPATH:/caminho/do/flaskmongo
export FLASK_APP=flaskmongo
export FLASK_ENV=development
flask run --reload
```

> Repare que há um diretório "flaskmongo" dentro de "flaskmongo". O PYTHONPATH deve apontar para "/caminho/do/flaskmongo" e não para "/caminho/do/flaskmongo/flaskmongo".

> **Importante**: Esta forma de execução é apenas para o ambiente de desenvolvimento. Não deve ser executado desta forma em produção.

Agora basta abrir no navegador o site [localhost:5000](http://localhost:5000).

Qualquer dúvida entre em contato: yoshiodeveloper@gmail.com