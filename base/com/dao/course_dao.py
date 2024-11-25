from base import db
from base.com.vo.course_vo import CourseVO
from base.com.vo.degree_vo import DegreeVO


class CourseDAO:
    def insert_course(self, course_vo):
        db.session.add(course_vo)
        db.session.commit()

    def view_course(self):
        course_vo_list = db.session.query(CourseVO, DegreeVO).join(
            DegreeVO,
            CourseVO.course_degree_id == DegreeVO.degree_id).all()
        return course_vo_list

    def delete_course(self, course_vo):
        course_vo_list = CourseVO.query.get(
            course_vo.course_id)
        db.session.delete(course_vo_list)
        db.session.commit()

    def edit_course(self, course_vo):
        course_vo_list = CourseVO.query.filter_by(course_id=
                                                  course_vo.course_id).all()
        return course_vo_list

    def update_course(self, course_vo):
        db.session.merge(course_vo)
        db.session.commit()

    def view_ajax_course(self, course_vo):
        course_vo_list = CourseVO.query.filter_by(
            course_degree_id=course_vo.course_degree_id).all()
        print("course_vo_list", course_vo_list)
        return course_vo_list
