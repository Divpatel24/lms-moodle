from datetime import timedelta

from flask import render_template, redirect, request, url_for, make_response, \
    flash

from base import app
from base.com.dao.assignment_dao import AssignmentDAO
from base.com.dao.course_dao import CourseDAO
from base.com.dao.degree_dao import DegreeDAO
from base.com.dao.exam_dao import ExamDAO
from base.com.dao.faculty_dao import FacultyDAO
from base.com.dao.lecture_dao import LectureDAO
from base.com.dao.login_dao import LoginDAO
from base.com.dao.semester_dao import SemesterDAO
from base.com.dao.student_dao import StudentDAO
from base.com.dao.subject_dao import SubjectDAO
from base.com.vo.assignment_vo import AssignmentVO
from base.com.vo.exam_vo import ExamVO
from base.com.vo.faculty_vo import FacultyVO
from base.com.vo.lecture_vo import LectureVO
from base.com.vo.login_vo import LoginVO
from base.com.vo.student_vo import StudentVO

global_loginvo_list = []
global_login_secretkey_set = {0}


@app.route('/', methods=['GET'])
def admin_load_login():
    try:
        return render_template('admin/login.html')
    except Exception as ex:
        print("admin_load_login route exception occured>>>>>>>>>>", ex)


@app.route('/admin/validate_login', methods=['POST'])
def admin_validate_login():
    try:
        global global_loginvo_list
        global global_login_secretkey_set

        login_username = request.form.get('loginUsername')
        login_password = request.form.get('loginPassword')

        login_vo = LoginVO()
        login_dao = LoginDAO()

        login_vo.login_username = login_username

        login_vo_list = login_dao.check_login_username(login_vo)
        login_list = [i.as_dict() for i in login_vo_list]
        len_login_list = len(login_list)
        if len_login_list == 0:
            error_message = 'username is incorrect !'
            flash(error_message)
            return redirect('/')
        elif not login_list[0]['login_status']:
            error_message = 'You have been temporarily blocked by website admin !'
            flash(error_message)
            return redirect('/')
        else:
            login_id = login_list[0]['login_id']
            login_username = login_list[0]['login_username']
            login_role = login_list[0]['login_role']
            login_secretkey = login_list[0]['login_secretkey']
            database_login_password = login_list[0]['login_password']
            if login_password == database_login_password:
                login_vo_dict = {
                    login_secretkey: {'login_username': login_username,
                                      'login_role': login_role,
                                      'login_id': login_id}}
                if len(global_loginvo_list) != 0:
                    for i in global_loginvo_list:
                        temp_list = list(i.keys())
                        global_login_secretkey_set.add(temp_list[0])
                    login_secretkey_list = list(global_login_secretkey_set)
                    if login_secretkey not in login_secretkey_list:
                        global_loginvo_list.append(login_vo_dict)
                else:
                    global_loginvo_list.append(login_vo_dict)
                if login_role == 'admin':
                    response = make_response(
                        redirect(url_for('admin_load_dashboard')))
                    response.set_cookie('login_secretkey',
                                        value=login_secretkey,
                                        max_age=timedelta(minutes=30))
                    response.set_cookie('login_username', value=login_username,
                                        max_age=timedelta(minutes=30))
                    return response
                elif login_role == 'faculty':
                    response = make_response(
                        redirect(url_for('faculty_load_dashboard')))
                    response.set_cookie('login_secretkey',
                                        value=login_secretkey,
                                        max_age=timedelta(minutes=30))
                    response.set_cookie('login_username', value=login_username,
                                        max_age=timedelta(minutes=30))
                    return response
                elif login_role == 'student':
                    response = make_response(
                        redirect(url_for('student_load_dashboard')))
                    response.set_cookie('login_secretkey',
                                        value=login_secretkey,
                                        max_age=timedelta(minutes=30))
                    response.set_cookie('login_username', value=login_username,
                                        max_age=timedelta(minutes=30))
                    return response
                else:
                    return redirect(url_for('admin_logout_session'))
            else:
                error_message = 'password is incorrect !'
                flash(error_message)
                return redirect('/')
    except Exception as ex:
        print("admin_validate_login route exception occured>>>>>>>>>>", ex)


@app.route('/admin/load_dashboard', methods=['GET'])
def admin_load_dashboard():
    try:
        if admin_login_session() == "admin":
            degree_dao = DegreeDAO()
            degree_vo_list = degree_dao.view_degree()
            degree_length = len(degree_vo_list)

            course_dao = CourseDAO()
            course_vo_list = course_dao.view_course()
            course_length = len(course_vo_list)

            semester_dao = SemesterDAO()
            semester_vo_list = semester_dao.view_semester()
            semester_length = len(semester_vo_list)

            subject_dao = SubjectDAO()
            subject_vo_list = subject_dao.view_subject()
            subject_length = len(subject_vo_list)

            faculty_dao = FacultyDAO()
            faculty_vo_list = faculty_dao.view_faculty()
            faculty_length = len(faculty_vo_list)

            student_dao = StudentDAO()
            student_vo_list = student_dao.view_student()
            student_length = len(student_vo_list)

            login_username = request.cookies.get('login_username')
            return render_template('admin/index.html',
                                   login_username=login_username,
                                   degree_length=degree_length,
                                   course_length=course_length,
                                   semester_length=semester_length,
                                   subject_length=subject_length,
                                   faculty_length=faculty_length,
                                   student_length=student_length)
        else:
            return redirect(url_for('admin_logout_session'))
    except Exception as ex:
        print("admin_load_dashboard route exception occured>>>>>>>>>>", ex)


@app.route('/faculty/load_dashboard', methods=['GET'])
def faculty_load_dashboard():
    try:
        if admin_login_session() == "faculty":
            login_vo = LoginVO()
            login_dao = LoginDAO()
            faculty_vo = FacultyVO()
            faculty_dao = FacultyDAO()

            # bringing faculty login id
            login_vo.login_username = request.cookies.get('login_username')
            faculty_login_id = login_dao.find_login_id(login_vo)

            # bringing faculty id
            faculty_vo.faculty_login_id = faculty_login_id
            faculty_id = faculty_dao.find_faculty_id(faculty_vo)

            faculty_vo.faculty_id = faculty_id
            faculty_course_id = faculty_dao.find_course_id(faculty_vo)

            # bringing assignment data based on faculty id
            assignment_vo = AssignmentVO()
            assignment_vo.assignment_faculty_id = faculty_id
            assignment_dao = AssignmentDAO()
            assignment_vo_list = assignment_dao.faculty_view_assignment(
                assignment_vo)
            assignment_length = len(assignment_vo_list)

            lecture_vo = LectureVO()
            lecture_vo.lecture_faculty_id = faculty_id
            lecture_dao = LectureDAO()
            lecture_vo_list = lecture_dao.faculty_view_lecture(lecture_vo)
            lecture_length = len(lecture_vo_list)

            exam_vo = ExamVO()
            exam_vo.exam_faculty_id = faculty_id
            exam_dao = ExamDAO()
            exam_vo_list = exam_dao.faculty_view_exam(exam_vo)
            exam_length = len(exam_vo_list)

            student_dao = StudentDAO()
            student_vo_list = student_dao.view_studentdata(
                faculty_course_id)
            student_length = len(student_vo_list)

            return render_template('faculty/index.html',
                                   assignment_length=assignment_length,
                                   lecture_length=lecture_length,
                                   exam_length=exam_length,
                                   student_length=student_length)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_load_dashboard route exception occured>>>>>>>>>>", ex)


@app.route('/student/load_dashboard', methods=['GET'])
def student_load_dashboard():
    try:
        if admin_login_session() == "student":
            login_vo = LoginVO()
            login_dao = LoginDAO()
            student_vo = StudentVO()
            student_dao = StudentDAO()
            faculty_dao = FacultyDAO()

            # bringing student login id
            login_vo.login_username = request.cookies.get('login_username')
            student_login_id = login_dao.find_login_id(login_vo)

            # bringing student id
            student_vo.student_login_id = student_login_id
            student_id = student_dao.find_student_id(student_vo)

            # bringing course id
            student_vo.student_id = student_id
            student_course_id = student_dao.find_course_id(student_vo)

            faculty_id = faculty_dao.find_faculty(student_course_id)

            # bringing faculty degree & course data
            faculty_vo_list = faculty_dao.view_facultydata(faculty_id)
            return render_template('student/index.html',
                                   faculty_vo_list=faculty_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("student_load_dashboard route exception occured>>>>>>>>>>", ex)


@app.route('/admin/login_session')
def admin_login_session():
    try:
        global global_loginvo_list
        login_role_flag = ""
        login_secretkey = request.cookies.get('login_secretkey')
        if login_secretkey is None:
            return redirect('/')
        for i in global_loginvo_list:
            if login_secretkey in i.keys():
                if i[login_secretkey]['login_role'] == 'admin':
                    login_role_flag = "admin"
                elif i[login_secretkey]['login_role'] == 'faculty':
                    login_role_flag = "faculty"
                elif i[login_secretkey]['login_role'] == 'student':
                    login_role_flag = "student"
        return login_role_flag
    except Exception as ex:
        print("admin_login_session route exception occured>>>>>>>>>>", ex)


@app.route("/admin/logout_session", methods=['GET'])
def admin_logout_session():
    try:
        global global_loginvo_list
        login_secretkey = request.cookies.get('login_secretkey')
        login_username = request.cookies.get('login_username')
        response = make_response(redirect('/'))
        if login_secretkey is not None and login_username is not None:
            response.set_cookie('login_secretkey', login_secretkey, max_age=0)
            response.set_cookie('login_username', login_username, max_age=0)
            for i in global_loginvo_list:
                if login_secretkey in i.keys():
                    global_loginvo_list.remove(i)
                    break
        return response
    except Exception as ex:
        print("admin_logout_session route exception occured>>>>>>>>>>", ex)

# @app.route('/admin/user_login', methods=['GET'])
# def admin_user_login():
#     try:
#         login_username = request.cookies.get('login_username')
#         return login_username
#     except Exception as ex:
#         print("admin_user_login route exception occured>>>>>>>>>>", ex)
