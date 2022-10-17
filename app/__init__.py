import os
import sqlalchemy
from yaml import load, Loader
from flask import Flask, render_template

app = Flask(__name__)
def db_init():

    if os.environ.get('GAE_ENV') != 'standard':
        try:
            variables = load(open("app.yaml"), Loader=Loader)
        except OSError as e:
            print("Make sure you have the app.yaml file setup")
            os.exit()

        env_variables = variables['env_variables']
        for var in env_variables:
            os.environ[var] = env_variables[var]
        
    db_engine = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername='postgresql',
            username=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD'),
            database=os.environ.get('POSTGRES_DB'),
            host=os.environ.get('POSTGRES_HOST')
        )
    )

    return db_engine

db = db_init()

from app import routes

