"""
Data model for Admin, inheriting from User.
"""
from dataclasses import dataclass
from source.college_erp.models.user import User, UserRole

@dataclass
class Admin(User):
    """
    Represents an Admin user.
    Corresponds to the Admin class in the class diagram.
    """
    def __init__(self, user_id: str, name: str, password: str):
        super().__init__(user_id, name, password, UserRole.ADMIN)