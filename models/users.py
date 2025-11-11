from datetime import date

class User:
    """Base class for shared attributes."""
    def __init__(self, u_id, name, password, role):
        self.id = u_id
        self.name = name
        self.password = password
        self.role = role

    def __repr__(self):
        return f"<{self.role}: {self.name} ({self.id})>"

class Student(User):
    """Implements Student entity."""
    def __init__(self, u_id, name, password, branch, cgpa=0.0, admission_date=None):
        super().__init__(u_id, name, password, "Student")
        self.branch = branch
        self.cgpa = cgpa
        self.date_of_admission = admission_date if admission_date else date.today()

class Admin(User):
    """Implements Admin entity."""
    def __init__(self, u_id, name, password):
        super().__init__(u_id, name, password, "Admin")

class Professor(User):
    """Implements Professor entity."""
    def __init__(self, u_id, name, password, branch):
        super().__init__(u_id, name, password, "Professor")
        self.branch = branch