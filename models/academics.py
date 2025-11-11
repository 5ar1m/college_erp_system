import uuid

class Course:
    """Implements Course entity."""
    def __init__(self, c_id, name, coordinator_id):
        self.id = c_id
        self.name = name
        self.coordinator_id = coordinator_id

    def __repr__(self):
        return f"<Course: {self.name} ({self.id})>"

class Enrollment:
    """Implements Enrollment entity."""
    def __init__(self, student_id, course_id):
        self.student_id = student_id
        self.course_id = course_id
        self.status = "Pending"

    def __repr__(self):
        return f"<Enrollment: {self.student_id}->{self.course_id} [{self.status}]>"

class Grade:
    """Implements Grade entity."""
    def __init__(self, student_id, course_id, grade_value):
        self.id = str(uuid.uuid4())[:8]
        self.student_id = student_id
        self.course_id = course_id
        self.grade_value = grade_value

    def __repr__(self):
        return f"<Grade: {self.student_id} in {self.course_id} = {self.grade_value}>"