"""
Data model for Professor, inheriting from User.
"""
from dataclasses import dataclass
from source.college_erp.models.user import User, UserRole

@dataclass
class Professor(User):
    """
    Represents a Professor user.
    Corresponds to the Professor class in the class diagram.
    """
    branch: str

    def __init__(self, user_id: str, name: str, password: str, branch: str):
        super().__init__(user_id, name, password, UserRole.PROFESSOR)
        self.branch = branch