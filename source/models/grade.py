"""
Data model for Grade.
"""
from dataclasses import dataclass

@dataclass
class Grade:
    """
    Represents a Grade.
    Corresponds to the Grade class in the class diagram.
    """
    grade_id: str
    student_id: str  # FK to Student.user_id
    course_id: str   # FK to Course.course_id
    grade_value: str # e.g., "A+", "B", "F"