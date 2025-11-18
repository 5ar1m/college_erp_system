"""
Data model for Student, inheriting from User.
"""
from dataclasses import dataclass
from datetime import date
from source.college_erp.models.user import User, UserRole

@dataclass
class Student(User):
    """
    Represents a Student user.
    Corresponds to the Student class in the class diagram.
    """
    cgpa: float
    date_of_admission: date
    branch: str

    def __init__(self, user_id: str, name: str, password: str, 
                 branch: str, cgpa: float = 0.0, date_of_admission: date = date.today()):
        super().__init__(user_id, name, password, UserRole.STUDENT)
        self.branch = branch
        self.cgpa = cgpa
        self.date_of_admission = date_of_admission