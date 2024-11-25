from base import db
from base.com.vo.course_vo import CourseVO
from base.com.vo.degree_vo import DegreeVO


class SemesterVO(db.Model):
    __tablename__ = 'semester_table'

    semester_id = db.Column('semester_id', db.Integer, primary_key=True,
                            autoincrement=True)
    semester_degree_id = db.Column('semester_degree_id', db.Integer,
                                   db.ForeignKey(DegreeVO.degree_id,
                                                 ondelete='CASCADE',
                                                 onupdate='CASCADE'),
                                   nullable=False)
    semester_course_id = db.Column('semester_course_id', db.Integer,
                                   db.ForeignKey(
                                       CourseVO.course_id,
                                       ondelete='CASCADE',
                                       onupdate='CASCADE'), nullable=False)
    semester_number = db.Column('semester_number', db.Integer, nullable=False)

    def as_dict(self):
        return {
            'semester_id': self.semester_id,
            'semester_degree_id': self.semester_degree_id,
            'semester_course_id': self.semester_course_id,
            'semester_number': self.semester_number,
        }


db.create_all()
