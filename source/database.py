"""
Mock Database for the College ERP System.
This simulates a real database (like the one in the ERD) 
using in-memory dictionaries.
"""
import copy
from typing import Dict, Optional, Any
from source.college_erp.models.user import User
from source.college_erp.models.course import Course
from source.college_erp.models.enrollment import Enrollment
from source.college_erp.models.grade import Grade

class Database:
    """
    A singleton-like class to simulate database tables.
    """
    def __init__(self):
        """Initializes the mock database tables as dictionaries."""
        self.users: Dict[str, User] = {}
        self.courses: Dict[str, Course] = {}
        self.enrollments: Dict[str, Enrollment] = {}
        self.grades: Dict[str, Grade] = {}

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Fetches a user by their ID."""
        return copy.deepcopy(self.users.get(user_id))

    def clear_all(self):
        """Clears all data from the mock database."""
        self.users.clear()
        self.courses.clear()
        self.enrollments.clear()
        self.grades.clear()

# A single instance to be used across the application
mock_db = Database()