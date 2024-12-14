from flask import Flask, g, jsonify
from db_connection import DBConnection
import uuid

import os

app = Flask(__name__)


db_config = {
    "host":  os.getenv('DB_CONNECTION_HOST', 'localhost'),
    "port": os.getenv('DB_CONNECTION_PORT', '32432'),
    "user": os.getenv('DB_USERNAME', 'postgres'),
    "password": os.getenv('DB_PASSWORD', 'postgres'),
    'database': os.getenv('DB_DATABASE', 'prediction_core')
}

db = DBConnection(
    dbname= db_config['database'],
    user=db_config["user"],
    password=db_config["password"],
    host=db_config["host"],
    port=db_config["port"]
)


@app.before_request
def before_request():
    """This function is executed before each request to set up the DB connection."""
    g.db_connection = db.get_connection()

@app.after_request
def after_request(response):
    """This function is executed after each request to release the DB connection."""
    db.release_connection(g.db_connection)
    return response

api_version = os.getenv('API_VERSION', 'v1')

@app.route("/api/version")
def apiV1():
    return "v1"


@app.route("/api/{0}/forecast/<jobId>".format(api_version), methods=['GET'])
def get_forecast(jobId):
    cursor = g.db_connection.cursor()
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    return jsonify({'jobId':jobId, 'PostgreSQL Version': db_version})

@app.route("/api/{0}/forecast".format(api_version), methods=['POST'])
def request_forecast():
    jobId = uuid.uuid4()
    return jsonify({'jobId': jobId})

if __name__ == "__main__":
    app.run()