# FOODGRAM

# About
The project is an API for service where users can create accounts, post recipes, followed by other users and save some of the other user's recipes in a favourites list.

# .env file

You need to add .env file to _infra_ directory. The example is below.

```PYTHON
DB_NAME= _database_name_
POSTGRES_USER= _database_user_
POSTGRES_PASSWORD= _database_password_
DB_HOST=db-test
DB_PORT=5432
SECRET_KEY = _secret_key_
```
The default database is Postgres. Specify it in .env as DB_ENGINE=... in case you need another.

# Getting started

The project was made using Django 4.0 and Python 3.7. Other necessary packajes are noticed in requirements.txt.


# Request examples

This API is documented and you can find request example at http://127.0.0.1:8000/redoc/ after running the server.