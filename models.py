import json


class Employee_:
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