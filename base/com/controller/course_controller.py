from flask import request, render_template, redirect, flash

from base import app
from base.com.controller.login_controller import admin_logout_session, \
    admin_login_session
from base.com.dao.course_dao import CourseDAO
from base.com.dao.degree_dao import DegreeDAO
from base.com.vo.course_vo import CourseVO


@app.route('/admin/load_course')
def admin_load_course():
    try:
        if admin_login_session() == "admin":
            degree_dao = DegreeDAO()
            degree_vo_list = degree_dao.view_degree()
            return render_template('admin/addCourse.html',
                                   degree_vo_list=degree_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_load_course route exception occured>>>>>>>>>>", ex)


@app.route('/admin/insert_course', methods=['POST'])
def admin_insert_course():
    try:
        if admin_login_session() == "admin":
            course_degree_id = request.form.get('courseDegreeId')
            course_name = request.form.get('courseName')
            course_code = request.form.get('courseCode')
            course_description = request.form.get('courseDescription')

            course_vo = CourseVO()
            course_dao = CourseDAO()

            course_vo.course_degree_id = course_degree_id
            course_vo.course_name = course_name
            course_vo.course_code = course_code
            course_vo.course_description = course_description

            course_dao.insert_course(course_vo)
            return redirect('/admin/view_course')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_add_course route exception occured>>>>>>>>>>", ex)


@app.route('/admin/view_course')
def admin_view_course():
    try:
        if admin_login_session() == "admin":
            course_dao = CourseDAO()
            course_vo_list = course_dao.view_course()
            return render_template('admin/viewCourse.html',
                                   course_vo_list=course_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_view_course route exception occured>>>>>>>>>>", ex)


@app.route('/admin/delete_course')
def admin_delete_course():
    try:
        if admin_login_session() == "admin":
            course_vo = CourseVO()
            course_dao = CourseDAO()

            course_id = request.args.get('courseId')
            course_vo.course_id = course_id
            course_dao.delete_course(course_vo)
            success_message = 'Record Deleted Successfully!'
            flash(success_message)
            return redirect('/admin/view_course')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_delete_course route exception occured>>>>>>>>>>", ex)


@app.route('/admin/edit_course')
def admin_edit_course():
    try:
        if admin_login_session() == "admin":
            degree_dao = DegreeDAO()
            degree_vo_list = degree_dao.view_degree()

            course_vo = CourseVO()
            course_dao = CourseDAO()

            course_id = request.args.get('courseId')
            course_vo.course_id = course_id
            course_vo_list = course_dao.edit_course(course_vo)
            print("|")
            print(course_vo_list)
            return render_template('admin/editCourse.html',
                                   course_vo_list=course_vo_list,
                                   degree_vo_list=degree_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_edit_course route exception occured>>>>>>>>>>", ex)


@app.route('/admin/update_course', methods=['POST'])
def admin_update_course():
    try:
        if admin_login_session() == "admin":
            course_id = request.form.get('courseId')
            course_degree_id = request.form.get('courseDegreeId')
            course_name = request.form.get('courseName')
            course_code = request.form.get('courseCode')
            course_description = request.form.get('courseDescription')

            course_vo = CourseVO()
            course_dao = CourseDAO()

            course_vo.course_id = course_id
            course_vo.course_degree_id = course_degree_id
            course_vo.course_name = course_name
            course_vo.course_code = course_code
            course_vo.course_description = course_description

            course_dao.update_course(course_vo)
            return redirect('/admin/view_course')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_update_course route exception occured>>>>>>>>>>", ex)
