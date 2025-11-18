"""
Data model for Enrollment.
"""
from dataclasses import dataclass
from enum import Enum

class EnrollmentStatus(Enum):
    """Status of a student's registration request."""
    PENDING = "Pending"
    ENROLLED = "Enrolled"
    REJECTED = "Rejected"

@dataclass
class Enrollment:
    """
    Represents an Enrollment record.
    Corresponds to the Enrollment class in the class diagram.
    Links a Student to a Course.
    """
    enrollment_id: str
    student_id: str  # FK to Student.user_id
    course_id: str   # FK to Course.course_id
    status: EnrollmentStatus = EnrollmentStatus.PENDING