"""
Base User model and Role enumeration.
"""
from dataclasses import dataclass
from enum import Enum

class UserRole(Enum):
    """Enumeration for user roles."""
    STUDENT = "student"
    PROFESSOR = "professor"
    ADMIN = "admin"

@dataclass
class User:
    """Base class for a user in the system."""
    user_id: str
    name: str
    password: str
    role: UserRole

    def check_password(self, password_to_check: str) -> bool:
        """Compares the provided password with the stored one."""
        return self.password == password_to_check