from base import db
from base.com.vo.course_vo import CourseVO
from base.com.vo.degree_vo import DegreeVO
from base.com.vo.semester_vo import SemesterVO


class SemesterDAO:
    def insert_semester(self, semester_vo):
        db.session.add(semester_vo)
        db.session.commit()

    def view_semester(self):
        semester_vo_list = db.session.query(DegreeVO, CourseVO,
                                            SemesterVO).filter(
            DegreeVO.degree_id == SemesterVO.semester_degree_id).filter(
            CourseVO.course_id ==
            SemesterVO.semester_course_id).all()
        return semester_vo_list

    def delete_semester(self, semester_vo):
        semester_vo_list = SemesterVO.query.get(semester_vo.semester_id)
        db.session.delete(semester_vo_list)
        db.session.commit()

    def edit_semester(self, semester_vo):
        semester_vo_list = SemesterVO.query.filter_by(semester_id=
                                                      semester_vo.semester_id).all()
        return semester_vo_list

    def update_semester(self, semester_vo):
        db.session.merge(semester_vo)
        db.session.commit()

    def view_ajax_semester(self, semester_vo):
        semester_vo_list = SemesterVO.query.filter_by(
            semester_course_id=semester_vo.semester_course_id).all()
        return semester_vo_list
