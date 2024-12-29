from flask import Flask, request
from flask.blueprints import Blueprint
from sqlalchemy.ext.declarative import declarative_base
from config import DB_CONFIG, API_VERSION
from models import db
from flasgger import Swagger
import routes

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{username}:{password}@{host}:{port}/{database}'.format(username=DB_CONFIG['username'], 
                                                                                                             password=DB_CONFIG['password'],
                                                                                                             host=DB_CONFIG['host'],
                                                                                                             port=DB_CONFIG['port'],
                                                                                                             database=DB_CONFIG['database']
                                                                                                            )
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable the modification tracking system to save resources


app.config["SWAGGER"] = {
    "swagger_version": "2.0",
    "title": "Application",
    "specs": [
        {
            "version": "0.0.1",
            "title": "Application",
            "endpoint": "spec",
            "route": "/application/spec",
            "rule_filter": lambda rule: True,  # all in
        }
    ],
    "static_url_path": "/apidocs",
}

Swagger(app)

db.init_app(app)
db.app = app

with app.app_context():
    db.create_all()

for blueprint in vars(routes).values():
    if isinstance(blueprint, Blueprint):
        app.register_blueprint(blueprint, url_prefix=f"/api/{API_VERSION}")

if __name__ == "__main__":
    app.run()