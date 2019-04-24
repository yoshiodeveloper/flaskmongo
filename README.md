# flaskmongo

Trabalho sobre MongoDB feito em Python e Flask.

## Instalação no Linux

* `É necessário ter o Python 3, virtualenv e MongoDB instalados.`

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

Execute a aplicação.

```shell
export PYTHONPATH=$PYTHONPATH:/caminho/do/flaskmongo
export FLASK_APP=flaskmongo
export FLASK_ENV=development
flask run --reload
```

- `Repare que há um diretório "flaskmongo" dentro de "flaskmongo". O PYTHONPATH deve apontar para "/caminho/do/flaskmongo" e não para "/caminho/do/flaskmongo/flaskmongo".`

Agora basta abrir no navegador o site [localhost:5000](http://localhost:5000).

Qualquer dúvida entre em contato: yoshiodeveloper@gmail.com