from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    exam_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Course {self.name}>"

class UserCourse(db.Model):
    __tablename__ = 'user_courses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)

    course = db.relationship("Course", backref="enrollments")

class UserPracticeGeneration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, nullable=False)
    unit_number = db.Column(db.Integer, nullable=False)
    last_generated = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'course_id', 'unit_number', name='unique_generation'),
    )