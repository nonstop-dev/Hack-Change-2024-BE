import os

from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy

SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'

app = Flask(__name__)

api = Api(app,
          default='Employees',
          default_label='Employee related operations',
          version='1.0.0-oas3',
          title='NonStop Hack&Change 2024',
          description='NonStop Hack&Change 2024 API',
          license='Apache 2.0',
          license_url='https://www.apache.org/licenses/LICENSE-2.0.html')

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'nonstop.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    nickname = db.Column(db.String(100), nullable=False)
    photoUrl = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(100), nullable=False)
    team = db.Column(db.String(100), nullable=True)
    department = db.Column(db.String(100), nullable=False)
    project = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    timezone = db.Column(db.String(100), nullable=True)
    skills = db.Column(db.String(255), nullable=True)
    workHours = db.Column(db.String(100), nullable=True)
    availability = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Employee {self.name}>'

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'nickname': self.nickname,
            'photoUrl': self.photoUrl,
            'role': self.role,
            'team': self.team,
            'department': self.department,
            'project': self.project,
            'city': self.city,
            'timezone': self.timezone,
            'skills': str(self.skills).split(','),
            'workHours': self.workHours,
            'availability': self.availability
        }

employee_model = api.model('Employee', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True, description='Name'),
    'email': fields.String(required=False, description='Email'),
    'nickname': fields.String(required=True, description='Nickname'),
    'photoUrl': fields.String(required=False, description='Photo URL'),
    'role': fields.String(required=True, description='Role'),
    'team': fields.String(required=False, description='Team'),
    'department': fields.String(required=True, description='Department'),
    'project': fields.String(required=False, description='Project'),
    'city': fields.String(required=False, description='City'),
    'timezone': fields.String(required=False, description='Timezone'),
    'skills': fields.List(fields.String(required=False, description='Skills')),
    'workHours': fields.String(required=False, description='Work Hours'),
    'availability': fields.String(required=False, description='Availability'),
})

# employees_ns = Namespace('Employees', description='Employee related operations')
# api.add_namespace(employees_ns)


@api.route('/employees')
class Employees(Resource):
    @api.doc(responses={200: 'Success'})
    @api.marshal_with(employee_model)
    def get(self):
        employees = Employee.query.all()
        return [e.to_json() for e in employees]


    @api.doc(responses={201: 'Created'},
             body=employee_model,
             validate=True)
    @api.marshal_with(employee_model)
    def post(self):
        data = request.json
        data['skills'] = ','.join(data.get('skills', []))
        new_employee = Employee(**data)
        db.session.add(new_employee)
        db.session.commit()
        return new_employee.to_json(), 201


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
