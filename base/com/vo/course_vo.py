from base import db
from base.com.vo.degree_vo import DegreeVO


class CourseVO(db.Model):
    __tablename__ = 'course_table'
    course_id = db.Column('course_id', db.Integer, primary_key=True,
                          autoincrement=True)
    course_degree_id = db.Column('course_degree_id', db.Integer,
                                 db.ForeignKey(DegreeVO.degree_id,
                                               ondelete='CASCADE',
                                               onupdate='CASCADE'),
                                 nullable=False)
    course_name = db.Column('course_name', db.String(255),
                            nullable=False)
    course_code = db.Column('course_code', db.String(3),
                            nullable=False)
    course_description = db.Column('course_description', db.Text,
                                   nullable=False)

    def as_dict(self):
        return {
            'course_id': self.course_id,
            'course_degree_id': self.course_degree_id,
            'course_name': self.course_name,
            'course_code': self.course_code,
            'course_description': self.course_description
        }


db.create_all()
