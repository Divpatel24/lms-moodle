from flask import request, render_template, redirect, jsonify, flash

from base import app
from base.com.controller.login_controller import admin_logout_session, \
    admin_login_session
from base.com.dao.course_dao import CourseDAO
from base.com.dao.degree_dao import DegreeDAO
from base.com.dao.semester_dao import SemesterDAO
from base.com.vo.course_vo import CourseVO
from base.com.vo.semester_vo import SemesterVO


@app.route('/admin/load_semester')
def admin_load_semester():
    try:
        if admin_login_session() == "admin":
            degree_dao = DegreeDAO()
            degree_vo_list = degree_dao.view_degree()

            return render_template('admin/addSemester.html',
                                   degree_vo_list=degree_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_load_Semester route exception occured>>>>>>>>>>", ex)


@app.route('/admin/ajax_course_semester')
def admin_ajax_course_semester():
    try:
        if admin_login_session() == "admin":
            course_vo = CourseVO()
            course_dao = CourseDAO()
            course_degree_id = request.args.get('semesterDegreeId')
            print("course_degree_id", course_degree_id)
            course_vo.course_degree_id = course_degree_id
            course_vo_list = course_dao.view_ajax_course(course_vo)
            print("course_vo_list", course_vo_list)
            ajax_semester_course = [i.as_dict() for i in
                                    course_vo_list]
            print("ajax_semester_course", ajax_semester_course)
            return jsonify(ajax_semester_course)
        else:
            return admin_logout_session()
    except Exception as ex:
        print(
            "admin_ajax_course_Semester route exception occured>>>>>>>>>>",
            ex)


@app.route('/admin/insert_semester', methods=['POST'])
def admin_insert_semester():
    try:
        if admin_login_session() == "admin":
            semester_degree_id = request.form.get('semesterDegreeId')
            semester_course_id = request.form.get('semesterCourseId')
            semester_number = request.form.get('semesterNumber')
            print("semester_course_id", semester_course_id)
            semester_vo = SemesterVO()
            semester_dao = SemesterDAO()

            semester_vo.semester_degree_id = semester_degree_id
            semester_vo.semester_course_id = semester_course_id
            semester_vo.semester_number = semester_number

            semester_dao.insert_semester(semester_vo)
            return redirect('/admin/view_semester')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_add_Semester route exception occured>>>>>>>>>>", ex)


@app.route('/admin/view_semester')
def admin_view_semester():
    try:
        if admin_login_session() == "admin":
            semester_dao = SemesterDAO()
            semester_vo_list = semester_dao.view_semester()
            print(semester_vo_list)
            return render_template('admin/viewSemester.html',
                                   semester_vo_list=semester_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_view_Semester route exception occured>>>>>>>>>>", ex)


@app.route('/admin/delete_semester')
def admin_delete_semester():
    try:
        if admin_login_session() == "admin":
            semester_vo = SemesterVO()
            semester_dao = SemesterDAO()

            semester_id = request.args.get('semesterId')
            semester_vo.semester_id = semester_id
            semester_dao.delete_semester(semester_vo)
            success_message = 'Record Deleted Successfully!'
            flash(success_message)
            return redirect('/admin/view_semester')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_delete_Semester route exception occured>>>>>>>>>>", ex)


@app.route('/admin/edit_semester')
def admin_edit_semester():
    try:
        if admin_login_session() == "admin":
            degree_dao = DegreeDAO()
            degree_vo_list = degree_dao.view_degree()

            course_dao = CourseDAO()
            course_vo_list = course_dao.view_course()

            semester_vo = SemesterVO()
            semester_dao = SemesterDAO()

            semester_id = request.args.get('semesterId')
            semester_vo.semester_id = semester_id
            semester_vo_list = semester_dao.edit_semester(semester_vo)
            return render_template('admin/editSemester.html', degree_vo_list=
            degree_vo_list, course_vo_list=course_vo_list,
                                   semester_vo_list=semester_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_edit_Semester route exception occured>>>>>>>>>>", ex)


@app.route('/admin/update_semester', methods=['POST'])
def admin_update_semester():
    try:
        if admin_login_session() == "admin":
            semester_id = request.form.get('semesterId')
            semester_degree_id = request.form.get('semesterDegreeId')
            semester_course_id = request.form.get('semesterCourseId')
            semester_number = request.form.get('semesterNumber')

            semester_vo = SemesterVO()
            semester_dao = SemesterDAO()

            semester_vo.semester_id = semester_id
            semester_vo.semester_degree_id = semester_degree_id
            semester_vo.semester_course_id = semester_course_id
            semester_vo.semester_number = semester_number

            semester_dao.update_semester(semester_vo)
            return redirect('/admin/view_semester')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_update_course route exception occured>>>>>>>>>>", ex)
