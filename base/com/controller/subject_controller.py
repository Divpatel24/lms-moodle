from flask import request, render_template, redirect, jsonify, flash

from base import app
from base.com.controller.login_controller import admin_login_session, \
    admin_logout_session
from base.com.dao.course_dao import CourseDAO
from base.com.dao.degree_dao import DegreeDAO
from base.com.dao.login_dao import LoginDAO
from base.com.dao.semester_dao import SemesterDAO
from base.com.dao.student_dao import StudentDAO
from base.com.dao.subject_dao import SubjectDAO
from base.com.vo.course_vo import CourseVO
from base.com.vo.login_vo import LoginVO
from base.com.vo.semester_vo import SemesterVO
from base.com.vo.student_vo import StudentVO
from base.com.vo.subject_vo import SubjectVO


@app.route('/admin/load_subject')
def admin_load_subject():
    try:
        if admin_login_session() == "admin":
            degree_dao = DegreeDAO()
            degree_vo_list = degree_dao.view_degree()

            return render_template('admin/addSubject.html',
                                   degree_vo_list=degree_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_load_Subject route exception occured>>>>>>>>>>", ex)


@app.route('/admin/ajax_course_subject')
def admin_ajax_course_subject():
    try:
        if admin_login_session() == "admin":
            course_vo = CourseVO()
            course_dao = CourseDAO()
            course_degree_id = request.args.get('subjectDegreeId')
            course_vo.course_degree_id = course_degree_id

            course_vo_list = course_dao.view_ajax_course(
                course_vo)
            ajax_subject_course = [i.as_dict() for i in course_vo_list]
            return jsonify(ajax_subject_course)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_ajax_course_Subject route exception occured>>>>>>>>>>",
              ex)


@app.route('/admin/ajax_semester_subject')
def admin_ajax_semester_subject():
    try:
        if admin_login_session() == "admin":
            semester_vo = SemesterVO()
            semester_dao = SemesterDAO()
            semester_course_id = request.args.get('subjectCourseId')
            semester_vo.semester_course_id = semester_course_id
            semester_vo_list = semester_dao.view_ajax_semester(semester_vo)
            ajax_subject_semester = [i.as_dict() for i in semester_vo_list]
            return jsonify(ajax_subject_semester)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_ajax_semester_Subject route exception "
              "occured>>>>>>>>>>", ex)


@app.route('/admin/insert_subject', methods=['POST'])
def admin_insert_subject():
    try:
        if admin_login_session() == "admin":
            subject_degree_id = request.form.get('subjectDegreeId')
            subject_course_id = request.form.get('subjectCourseId')
            subject_semester_id = request.form.get('subjectSemesterId')
            subject_name = request.form.get('subjectName')
            subject_code = request.form.get('subjectCode')
            subject_textbook = request.form.get('subjectTextbook')

            subject_vo = SubjectVO()
            subject_dao = SubjectDAO()

            subject_vo.subject_degree_id = subject_degree_id
            subject_vo.subject_course_id = subject_course_id
            subject_vo.subject_semester_id = subject_semester_id
            subject_vo.subject_name = subject_name
            subject_vo.subject_code = subject_code
            subject_vo.subject_textbook = subject_textbook

            subject_dao.insert_subject(subject_vo)
            return redirect('/admin/view_subject')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_add_Subject route exception occured>>>>>>>>>>", ex)


@app.route('/admin/view_subject')
def admin_view_subject():
    try:
        if admin_login_session() == "admin":
            subject_dao = SubjectDAO()
            subject_vo_list = subject_dao.view_subject()
            print(">>>>>>>", subject_vo_list)
            return render_template('admin/viewSubject.html',
                                   subject_vo_list=subject_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_view_Subject route exception occured>>>>>>>>>>", ex)


@app.route('/admin/delete_subject')
def admin_delete_subject():
    try:
        if admin_login_session() == "admin":
            subject_vo = SubjectVO()
            subject_dao = SubjectDAO()

            subject_id = request.args.get('subjectId')
            subject_vo.subject_id = subject_id
            subject_dao.delete_subject(subject_vo)
            success_message = 'Record Deleted Successfully!'
            flash(success_message)
            return redirect('/admin/view_subject')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_delete_Subject route exception occured>>>>>>>>>>", ex)


@app.route('/admin/edit_subject')
def admin_edit_subject():
    try:
        if admin_login_session() == "admin":
            degree_dao = DegreeDAO()
            degree_vo_list = degree_dao.view_degree()

            # course_dao = CourseDAO()
            # course_vo_list = course_dao.view_course()
            #
            # semester_dao = SemesterDAO()
            # semester_vo_list = semester_dao.view_semester()

            subject_vo = SubjectVO()
            subject_dao = SubjectDAO()

            subject_id = request.args.get('subjectId')
            subject_vo.subject_id = subject_id
            subject_vo_list = subject_dao.edit_subject(subject_vo)
            return render_template('admin/editSubject.html',
                                   degree_vo_list=degree_vo_list,
                                   subject_vo_list=subject_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_edit_Subject route exception occured>>>>>>>>>>", ex)


@app.route('/admin/update_subject', methods=['POST'])
def admin_update_subject():
    try:
        if admin_login_session() == "admin":
            subject_id = request.form.get('subjectId')
            subject_degree_id = request.form.get('subjectDegreeId')
            subject_course_id = request.form.get('subjectCourseId')
            subject_semester_id = request.form.get('subjectSemesterId')
            subject_name = request.form.get('subjectName')
            subject_code = request.form.get('subjectCode')
            subject_textbook = request.form.get('subjectTextbook')

            subject_vo = SubjectVO()
            subject_dao = SubjectDAO()

            subject_vo.subject_id = subject_id
            subject_vo.subject_degree_id = subject_degree_id
            subject_vo.subject_course_id = subject_course_id
            subject_vo.subject_semester_id = subject_semester_id
            subject_vo.subject_name = subject_name
            subject_vo.subject_code = subject_code
            subject_vo.subject_textbook = subject_textbook

            subject_dao.update_subject(subject_vo)
            return redirect('/admin/view_subject')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_update_Subject route exception occured>>>>>>>>>>", ex)


@app.route('/student/view_subject')
def student_view_subject():
    try:
        if admin_login_session() == "student":
            login_vo = LoginVO()
            login_dao = LoginDAO()
            student_vo = StudentVO()
            student_dao = StudentDAO()
            subject_vo = SubjectVO()
            subject_dao = SubjectDAO()

            # bringing student login id
            login_vo.login_username = request.cookies.get('login_username')
            student_login_id = login_dao.find_login_id(login_vo)

            # bringing student id
            student_vo.student_login_id = student_login_id
            student_id = student_dao.find_student_id(student_vo)

            # bringing semester id
            student_vo.student_id = student_id
            student_semester_id = student_dao.find_semester_id(student_vo)

            # bringing all the data
            subject_vo.subject_semester_id = student_semester_id
            subject_vo_list = subject_dao.view_ajax_subject_faculty(
                subject_vo)

            return render_template('student/viewSubject.html',
                                   subject_vo_list=subject_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("student_load_student route exception occured>>>>>>>>>>", ex)
