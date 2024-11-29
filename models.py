# class Team:
#     def __init__(self, id, name, employees, manager):
#         self.id = id
#         self.name = name
#         self.employees = employees
#         self.manager = manager

# class Departments:
#     def __init___(self, id, name):
#         self.id = id
#         self.name = name
import json

class Employee:
    def __init__(
            self,
            name,
            photoUrl,
            nickname,
            role,
            team,
            department,
            project,
            city,
            timezone,
            skills,
            workHours,
            availability):
        self.name = name
        self.photoUrl = photoUrl
        self.nickname = nickname
        self.role = role
        self.team = team
        self.department = department
        self.project = project
        self.city = city
        self.timezone = timezone
        self.skills = skills
        self.workHours = workHours
        self.availability = availability

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)
