"""
Data model for Course.
"""
from dataclasses import dataclass, field

@dataclass
class Course:
    """
    Represents a Course.
    Corresponds to the Course class in the class diagram.
    """
    course_id: str
    name: str
    coordinator_id: str  # FK to Professor.user_id