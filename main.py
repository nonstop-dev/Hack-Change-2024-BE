from flask import Flask, jsonify, request
from api.internal import internal
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'
API_URL = '/swagger.json'

app = Flask(__name__)
app.register_blueprint(internal)
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "NonStop Hack And Change"
    }
)
app.register_blueprint(swaggerui_blueprint)

app.run()