
from flask import Blueprint, jsonify, request
from data_generator import generate_employees
import json

internal = Blueprint("stations_api", __name__)

@internal.route('/generateemployees', methods=['GET'])
def get_employees():
    employees = generate_employees(100)
    json_string = json.dumps([ob.__dict__ for ob in employees], ensure_ascii=False)
    return json_string