from base import db
from base.com.vo.course_vo import CourseVO
from base.com.vo.degree_vo import DegreeVO
from base.com.vo.login_vo import LoginVO
from base.com.vo.semester_vo import SemesterVO
from base.com.vo.student_vo import StudentVO


class StudentDAO:
    def insert_student(self, student_vo):
        db.session.add(student_vo)
        db.session.commit()

    def view_student(self):
        student_vo_list = db.session.query(DegreeVO, CourseVO,
                                           SemesterVO, LoginVO,
                                           StudentVO).filter(
            DegreeVO.degree_id == StudentVO.student_degree_id).filter(
            CourseVO.course_id ==
            StudentVO.student_course_id).filter(SemesterVO.semester_id
                                                ==
                                                StudentVO.student_semester_id).filter(
            LoginVO.login_id == StudentVO.student_login_id).all()
        return student_vo_list

    def delete_student(self, student_vo):
        student_vo_list = StudentVO.query.get(student_vo.student_id)
        db.session.delete(student_vo_list)
        db.session.commit()
        return student_vo_list

    def edit_student(self, student_vo):
        student_vo_list = db.session.query(StudentVO, LoginVO).filter_by(
            student_id=student_vo.student_id).filter(
            LoginVO.login_id == StudentVO.student_login_id).first()
        return student_vo_list

    def update_student(self, student_vo):
        db.session.merge(student_vo)
        db.session.commit()

    def view_studentdata(self, faculty_course_id):
        student_vo_list = db.session.query(StudentVO, DegreeVO, CourseVO,
                                           SemesterVO, LoginVO).filter_by(
            student_course_id=faculty_course_id).filter(
            DegreeVO.degree_id == StudentVO.student_degree_id).filter(
            CourseVO.course_id ==
            StudentVO.student_course_id).filter(SemesterVO.semester_id
                                                ==
                                                StudentVO.student_semester_id).filter(
            LoginVO.login_id == StudentVO.student_login_id).all()
        return student_vo_list

    def find_student_id(self, student_vo):
        student_vo_list = StudentVO.query.filter_by(
            student_login_id=student_vo.student_login_id).all()[-1].student_id
        return student_vo_list

    def find_course_id(self, student_vo):
        student_vo_list = StudentVO.query.filter_by(
            student_id=student_vo.student_id).all()[-1].student_course_id
        return student_vo_list

    def find_semester_id(self, student_vo):
        student_vo_list = StudentVO.query.filter_by(
            student_id=student_vo.student_id).all()[-1].student_semester_id
        return student_vo_list

    def load_studentdata(self, student_id):
        student_vo_list = db.session.query(StudentVO, DegreeVO, CourseVO,
                                           SemesterVO, LoginVO).filter_by(
            student_id=student_id).filter(
            DegreeVO.degree_id == StudentVO.student_degree_id).filter(
            CourseVO.course_id ==
            StudentVO.student_course_id).filter(SemesterVO.semester_id
                                                ==
                                                StudentVO.student_semester_id).filter(
            LoginVO.login_id == StudentVO.student_login_id).all()
        return student_vo_list
