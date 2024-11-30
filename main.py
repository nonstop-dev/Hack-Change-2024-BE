import json

from flask import Flask, jsonify
from flask_restx import Api, Resource, fields, Namespace

SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'

app = Flask(__name__)
api = Api(app,
          version='1.0.0-oas3',
          title='NonStop Hack&Change 2024',
          description='NonStop Hack&Change 2024 API',
          license='Apache 2.0',
          license_url='https://www.apache.org/licenses/LICENSE-2.0.html')

employee_model = api.model('Employee', {
    'name': fields.String(required=True, description='Name'),
    'nickname': fields.String(required=True, description='Nickname'),
    'photoUrl': fields.String(required=False, description='Photo URL'),
    'role': fields.String(required=True, description='Role'),
    'team': fields.String(required=False, description='Team'),
    'department': fields.String(required=True, description='Department'),
    'project': fields.String(required=False, description='Project'),
    'city': fields.String(required=False, description='City'),
    'timezone': fields.String(required=False, description='Timezone'),
    'skills': fields.List(fields.String(required=False, description='Skills')),
    'workHours': fields.List(fields.String(required=False, description='Work Hours')),
    'availability': fields.List(fields.String(required=False, description='Availability')),
})

employees_ns = Namespace('Employees', description='Employee related operations')
api.add_namespace(employees_ns)


@employees_ns.route('/')
class Employees(Resource):
    @api.doc(responses={200: 'Success'})
    def get(self):
        employees_file = './employees.json'
        try:
            with open(employees_file, 'r') as file:
                data = json.load(file)

            return jsonify(data)
        except FileNotFoundError:
            return jsonify({"error": f"File not found: {employees_file}"}), 404
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON in file"}), 400

    @api.doc(responses={201: 'Created'},
             body=employee_model,
             validate=True)
    @api.marshal_with(employee_model)
    def post(self):
        # Create a new user
        return {'name': 'newuser', 'nickname': 'new@example.com'}, 201


if __name__ == '__main__':
    app.run(debug=True)
