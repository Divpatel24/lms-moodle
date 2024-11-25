from base import db
from base.com.vo.course_vo import CourseVO
from base.com.vo.degree_vo import DegreeVO
from base.com.vo.login_vo import LoginVO
from base.com.vo.semester_vo import SemesterVO


class StudentVO(db.Model):
    __tablename__ = 'student_table'
    student_id = db.Column('student_id', db.Integer, primary_key=True,
                           autoincrement=True)
    student_degree_id = db.Column('student_degree_id', db.Integer,
                                  db.ForeignKey(DegreeVO.degree_id,
                                                ondelete='CASCADE',
                                                onupdate='CASCADE'),
                                  nullable=False)
    student_course_id = db.Column('student_course_id', db.Integer,
                                  db.ForeignKey(
                                      CourseVO.course_id,
                                      ondelete='CASCADE',
                                      onupdate='CASCADE'), nullable=False)
    student_semester_id = db.Column('student_subject_id', db.Integer,
                                    db.ForeignKey(SemesterVO.semester_id,
                                                  ondelete='CASCADE',
                                                  onupdate='CASCADE'),
                                    nullable=False)
    student_login_id = db.Column('student_login_id', db.Integer,
                                 db.ForeignKey(LoginVO.login_id,
                                               ondelete='CASCADE',
                                               onupdate='CASCADE'),
                                 nullable=False)
    student_enrollment = db.Column('student_enrollment', db.String(15),
                                   nullable=False, unique=True)
    student_firstname = db.Column('student_firstname', db.String(255),
                                  nullable=False)
    student_lastname = db.Column('student_lastname', db.String(255),
                                 nullable=False)
    student_gender = db.Column('student_gender', db.String(10),
                               nullable=False)
    student_contact = db.Column('student_contact', db.String(10),
                                nullable=False)
    student_parent_contact = db.Column('student_parent_contact', db.String(10),
                                       nullable=False)
    student_dob = db.Column('student_dob', db.String(10),
                            nullable=False)
    student_image_name = db.Column('student_image_name', db.String(255),
                                   nullable=False)
    student_image_path = db.Column('student_image_path', db.String(255),
                                   nullable=False)

    def as_dict(self):
        return {
            'student_id': self.student_id,
            'student_degree_id': self.student_degree_id,
            'student_course_id': self.student_course_id,
            'student_login_id': self.student_login_id,
            'student_semester_id': self.student_semester_id,
            'student_enrollment': self.student_enrollment,
            'student_firstname': self.student_firstname,
            'student_lastname': self.student_lastname,
            'student_gender': self.student_gender,
            'student_contact': self.student_contact,
            'student_parent_contact': self.student_parent_contact,
            'student_dob': self.student_dob,
            'student_image_name': self.student_image_name,
            'student_image_path': self.student_image_path
        }


db.create_all()
