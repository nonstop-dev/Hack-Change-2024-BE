import os

from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy

from data_generator import generate_employees

SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'nonstop.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RESTX_MASK_SWAGGER'] = False

api = Api(app,
          default='Employees',
          default_label='Employee related operations',
          version='1.0.0-oas3',
          title='NonStop Hack&Change 2024',
          description='NonStop Hack&Change 2024 API',
          license='Apache 2.0',
          license_url='https://www.apache.org/licenses/LICENSE-2.0.html')

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

    @staticmethod
    def searchable_fields():
        return ['name', 'email', 'nickname', 'role', 'team', 'department', 'project', 'city', 'skills', 'timezone']



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


@api.route('/employees')
class EmployeesResource(Resource):
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


@api.route('/employees/<int:employee_id>')
class EmployeeResource(Resource):
    @api.doc(responses={200: 'Success'})
    @api.marshal_with(employee_model)
    def get(self, employee_id):
        employee = Employee.query.get_or_404(employee_id)
        return employee.to_json()

    @api.doc(responses={204: 'Updated'},
             body=employee_model,
             validate=True)
    def put(self, employee_id):
        employee = Employee.query.get_or_404(employee_id)
        employee.name = request.json.get('name') or employee.name
        employee.email = request.json.get('email') or employee.email
        employee.nickname = request.json.get('nickname') or employee.nickname
        employee.photoUrl = request.json.get('photoUrl') or employee.photoUrl
        employee.role = request.json.get('role') or employee.role
        employee.team = request.json.get('team') or employee.team
        employee.department = request.json.get('department') or employee.department
        employee.project = request.json.get('project') or employee.project
        employee.city = request.json.get('city') or employee.city
        employee.timezone = request.json.get('timezone') or employee.timezone
        skills = request.json.get('skills')
        skills = ','.join(skills) if skills else employee.skills
        employee.skills = skills
        employee.workHours = request.json.get('workHours') or employee.workHours
        employee.availability = request.json.get('availability') or employee.availability
        db.session.commit()
        return '', 204

    @api.response(204, 'Deleted')
    def delete(self, employee_id):
        employee = Employee.query.get_or_404(employee_id)
        db.session.delete(employee)
        db.session.commit()
        return '', 204


@api.route('/employees/search')
class EmployeeSearch(Resource):
    @api.param('q', 'Search query by name or nickname')
    @api.param('name', 'Full name')
    @api.param('email', 'Email')
    @api.param('nickname', 'Nickname')
    @api.param('role', 'Role')
    @api.param('team', 'Team')
    @api.param('department', 'Department')
    @api.param('project', 'Project')
    @api.param('city', 'City')
    @api.param('skills', 'Skills')
    @api.param('timezone', 'Timezone')
    @api.marshal_with(employee_model)
    def get(self):
        q = request.args.get('q', '').lower()
        employees =  [e.to_json() for e in Employee.query.all() if not q or q in e.name.lower() or q in e.nickname.lower()]
        for field in Employee.searchable_fields():
            field_filter = request.args.get(field)
            if field_filter:
                field_filter = field_filter.lower()
                if field == 'skills':
                    employees = [e for e in employees if field_filter in map(str.lower, e['skills'])]
                else:
                    employees = [e for e in employees if field_filter in e[field].lower()]

        return employees


@api.route('/internal/employees/generate', doc=False)
class InternalResource(Resource):
    def get(self):
        count = request.args.get('count', 100, int)
        employees = generate_employees(count)
        for employee in employees:
            new_employee = Employee(**employee)
            db.session.add(new_employee)

        db.session.commit()
        return '', 204

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
