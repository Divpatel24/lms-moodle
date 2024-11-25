import os

from flask import request, render_template, redirect, flash, jsonify
from werkzeug.utils import secure_filename

from base import app
from base.com.controller.login_controller import admin_login_session, \
    admin_logout_session
from base.com.dao.assignment_dao import AssignmentDAO
from base.com.dao.faculty_dao import FacultyDAO
from base.com.dao.login_dao import LoginDAO
from base.com.dao.semester_dao import SemesterDAO
from base.com.dao.student_dao import StudentDAO
from base.com.dao.subject_dao import SubjectDAO
from base.com.vo.assignment_vo import AssignmentVO
from base.com.vo.faculty_vo import FacultyVO
from base.com.vo.login_vo import LoginVO
from base.com.vo.semester_vo import SemesterVO
from base.com.vo.student_vo import StudentVO
from base.com.vo.subject_vo import SubjectVO

ASSIGNMENT_FOLDER = 'base/static/adminResources/assignment/'
app.config['ASSIGNMENT_FOLDER'] = ASSIGNMENT_FOLDER


@app.route('/faculty/load_assignment')
def faculty_load_assignment():
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

            # bringing faculty course id
            faculty_vo.faculty_id = faculty_id
            faculty_course_id = faculty_dao.find_course_id(faculty_vo)

            # bringing faculty degree & course data
            faculty_vo_list = faculty_dao.view_facultydata(faculty_id)

            # bringing semester based on course id
            semester_vo = SemesterVO()
            semester_dao = SemesterDAO()
            semester_vo.semester_course_id = faculty_course_id
            semester_dao_list = semester_dao.view_ajax_semester(semester_vo)

            return render_template('faculty/addAssignment.html',
                                   faculty_vo_list=faculty_vo_list,
                                   semester_dao_list=semester_dao_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_load_Subject route exception occured>>>>>>>>>>", ex)


@app.route('/faculty/insert_assignment', methods=['POST'])
def faculty_insert_assignment():
    try:
        if admin_login_session() == "faculty":
            assignment_vo = AssignmentVO()
            assignment_dao = AssignmentDAO()

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

            # bringing the data from ui
            assignment_semester_id = request.form.get('assignmentSemesterId')
            assignment_subject_id = request.form.get('assignmentSubjectId')
            assignment_title = request.form.get('assignmentTitle')
            assignment_start_date = request.form.get('assignmentStartDate')
            assignment_end_date = request.form.get('assignmentEndDate')
            assignment_description = request.form.get('assignmentDescription')
            assignment_marks = request.form.get('assignmentMarks')
            assignment_image = request.files.get('assignmentImage')
            assignment_image_name = secure_filename(assignment_image.filename)
            assignment_image_path = os.path.join(
                app.config['ASSIGNMENT_FOLDER'])
            assignment_image.save(os.path.join(assignment_image_path,
                                               assignment_image_name))

            # storing the data in database
            assignment_vo.assignment_semester_id = assignment_semester_id
            assignment_vo.assignment_subject_id = assignment_subject_id
            assignment_vo.assignment_faculty_id = faculty_id
            assignment_vo.assignment_title = assignment_title
            assignment_vo.assignment_startdate = assignment_start_date
            assignment_vo.assignment_enddate = assignment_end_date
            assignment_vo.assignment_description = assignment_description
            assignment_vo.assignment_marks = assignment_marks
            assignment_vo.assignment_image_name = assignment_image_name
            assignment_vo.assignment_image_path = assignment_image_path.replace(
                "base", "..")

            assignment_dao.insert_assignment(assignment_vo)
            return redirect('/faculty/view_assignment')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_insert_assignment route exception "
              "occured>>>>>>>>>>>>>", ex)


@app.route('/faculty/view_assignment')
def faculty_view_assignment():
    try:
        if admin_login_session() == "faculty":
            assignment_vo = AssignmentVO()
            assignment_dao = AssignmentDAO()

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

            # bringing assignment data based on faculty id
            assignment_vo.assignment_faculty_id = faculty_id
            assignment_vo_list = assignment_dao.faculty_view_assignment(
                assignment_vo)

            return render_template('faculty/viewAssignment.html',
                                   assignment_vo_list=assignment_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_view_assignment route exception occured>>>>>>>>>>", ex)


@app.route('/faculty/delete_assignment')
def faculty_delete_assignment():
    try:
        if admin_login_session() == "faculty":
            assignment_vo = AssignmentVO()
            assignment_dao = AssignmentDAO()

            # deleting assignment data from database
            assignment_id = request.args.get('assignmentId')
            assignment_vo.assignment_id = assignment_id
            assignment_vo_list = assignment_dao.delete_assignment(
                assignment_vo)

            # deleting assignment file
            file_path = assignment_vo_list.assignment_image_path.replace(
                "..", "base") + assignment_vo_list.assignment_image_name
            os.remove(file_path)

            success_message = 'Record Deleted Successfully!'
            flash(success_message)
            return redirect('/faculty/view_assignment')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_delete_assignment route exception occured>>>>>>>>>>",
              ex)


@app.route('/faculty/edit_assignment')
def faculty_edit_assignment():
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

            # bringing faculty course id
            faculty_vo.faculty_id = faculty_id
            faculty_course_id = faculty_dao.find_course_id(faculty_vo)

            # bringing faculty degree & course
            faculty_vo_list = faculty_dao.view_facultydata(faculty_id)

            # bringing semester based on course id
            semester_vo = SemesterVO()
            semester_dao = SemesterDAO()
            semester_vo.semester_course_id = faculty_course_id
            semester_dao_list = semester_dao.view_ajax_semester(semester_vo)

            # bringing assignment data to edit
            assignment_vo = AssignmentVO()
            assignment_dao = AssignmentDAO()
            assignment_id = request.args.get('assignmentId')
            assignment_vo.assignment_id = assignment_id
            assignment_vo_list = assignment_dao.edit_assignment(assignment_vo)
            return render_template('faculty/editAssignment.html',
                                   faculty_vo_list=faculty_vo_list,
                                   semester_dao_list=semester_dao_list,
                                   assignment_vo_list=assignment_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_edit_assignment route exception occured>>>>>>>>>>>>",
              ex)


@app.route('/faculty/update_assignment', methods=['POST'])
def faculty_update_assignment():
    try:
        if admin_login_session() == "faculty":
            assignment_vo = AssignmentVO()
            assignment_dao = AssignmentDAO()

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

            # bringing assignment data from ui
            assignment_id = request.form.get('assignmentId')

            assignment_semester_id = request.form.get('assignmentSemesterId')
            assignment_subject_id = request.form.get('assignmentSubjectId')
            assignment_title = request.form.get('assignmentTitle')
            assignment_start_date = request.form.get('assignmentStartDate')
            assignment_end_date = request.form.get('assignmentEndDate')
            assignment_description = request.form.get('assignmentDescription')
            assignment_marks = request.form.get('assignmentMarks')

            # storing all the data in database
            assignment_vo.assignment_semester_id = assignment_semester_id
            assignment_vo.assignment_id = assignment_id
            assignment_vo.assignment_subject_id = assignment_subject_id
            assignment_vo.assignment_faculty_id = faculty_id
            assignment_vo.assignment_title = assignment_title
            assignment_vo.assignment_startdate = assignment_start_date
            assignment_vo.assignment_enddate = assignment_end_date
            assignment_vo.assignment_description = assignment_description
            assignment_vo.assignment_marks = assignment_marks

            assignment_dao.update_assignment(assignment_vo)
            return redirect('/faculty/view_assignment')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_insert_assignment route exception "
              "occured>>>>>>>>>>>>>", ex)


@app.route('/faculty/ajax_subject_assignment')
def faculty_ajax_subject_assignment():
    try:
        if admin_login_session() == "faculty":
            subject_vo = SubjectVO()
            subject_dao = SubjectDAO()
            subject_semester_id = request.args.get('assignmentSemesterId')
            print("assignmentSemesterId>>>>>>>>>>>", subject_semester_id)
            subject_vo.subject_semester_id = subject_semester_id

            subject_vo_list = subject_dao.view_ajax_subject_faculty(subject_vo)
            print("subject_vo_list>>>>>>>>>>>>", subject_vo_list)
            ajax_assignment_subject = [i.as_dict() for i in subject_vo_list]
            return jsonify(ajax_assignment_subject)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("faculty_ajax_subject_assignment route exception "
              "occured>>>>>>>>>>", ex)


@app.route('/student/view_assignment')
def student_view_assignment():
    try:
        if admin_login_session() == "student":
            assignment_vo = AssignmentVO()
            assignment_dao = AssignmentDAO()

            login_vo = LoginVO()
            login_dao = LoginDAO()
            student_vo = StudentVO()
            student_dao = StudentDAO()

            # bringing login id
            login_vo.login_username = request.cookies.get(
                'login_username')
            student_login_id = login_dao.find_login_id(login_vo)

            # bringing student id
            student_vo.student_login_id = student_login_id
            student_id = student_dao.find_student_id(student_vo)

            # bringing semester id
            student_vo.student_id = student_id
            student_semester_id = student_dao.find_semester_id(
                student_vo)

            # bringing all the data
            assignment_vo.assignment_semester_id = student_semester_id
            assignment_vo_list = assignment_dao.student_view_assignment(
                assignment_vo)

            return render_template('student/viewassignment.html',
                                   assignment_vo_list=assignment_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("student_view_assignment route exception occured>>>>>>>>>>",
              ex)


@app.route('/student/upload_assignment')
def student_upload_assignment():
    try:
        if admin_login_session() == "student":
            login_vo = LoginVO()
            login_dao = LoginDAO()
            student_vo = StudentVO()
            student_dao = StudentDAO()
            assignment_dao = AssignmentDAO()

            # bringing student login id
            login_vo.login_username = request.cookies.get('login_username')
            student_login_id = login_dao.find_login_id(login_vo)

            # bringing student id
            student_vo.student_login_id = student_login_id
            student_id = student_dao.find_student_id(student_vo)

            # bringing course id
            student_vo.student_id = student_id
            student_semester_id = student_dao.find_semester_id(student_vo)

            assignment_id = assignment_dao.find_assignment(
                student_semester_id)

            print("assignment_id>>>>>>>>>>", assignment_id)

            # bringing faculty degree & course data
            assignment_vo_list = assignment_dao.view_assignmentdata(
                assignment_id)
            print("assignment_vo_list>>>>>>>>>>>", assignment_vo_list)

            return render_template('student/uploadAssignment.html',
                                   assignment_vo_list=assignment_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("student_view_assignment route exception occured>>>>>>>>>>",
              ex)





        # @app.route('/faculty/ajax_course_assignment')
        # def faculty_ajax_course_assignment():
        #     try:
        #         if admin_login_session() == "faculty":
        #             course_vo = CourseVO()
        #             course_dao = CourseDAO()
        #             course_degree_id = request.args.get('assignmentDegreeId')
        #             course_vo.course_degree_id = course_degree_id
        #
        #             course_vo_list = course_dao.view_ajax_course(
        #                 course_vo)
        #             ajax_assignment_course = [i.as_dict() for i in
        #                                           course_vo_list]
        #             return jsonify(ajax_assignment_course)
        #         else:
        #             return admin_logout_session()
        #     except Exception as ex:
        #         print("faculty_ajax_course_assignment route exception "
        #               "occured>>>>>>>>>>", ex)
        #
        #
        # @app.route('/faculty/ajax_subject_assignment')
        # def faculty_ajax_subject_assignment():
        #     try:
        #         if admin_login_session() == "faculty":
        #             subject_vo = SubjectVO()
        #             subject_dao = SubjectDAO()
        #             subject_course_id = request.args.get('assignmentCourseId')
        #             subject_vo.subject_course_id = subject_course_id
        #
        #             subject_vo_list = subject_dao.view_ajax_subject(subject_vo)
        #             ajax_assignment_subject = [i.as_dict() for i in subject_vo_list]
        #             return jsonify(ajax_assignment_subject)
        #         else:
        #             return admin_logout_session()
        #     except Exception as ex:
        #         print("faculty_ajax_subject_assignment route exception "
        #               "occured>>>>>>>>>>", ex)
        #
        #
        # @app.route('/faculty/ajax_faculty_assignment')
        # def faculty_ajax_faculty_assignment():
        #     try:
        #         if admin_login_session() == "faculty":
        #             faculty_vo = FacultyVO()
        #             faculty_dao = FacultyDAO()
        #             faculty_subject_id = request.args.get('assignmentSubjectId')
        #             faculty_vo.faculty_subject_id = faculty_subject_id
        #
        #             faculty_vo_list = faculty_dao.view_ajax_faculty(faculty_vo)
        #             ajax_assignment_faculty = [i.as_dict() for i in faculty_vo_list]
        #             return jsonify(ajax_assignment_faculty)
        #         else:
        #             return admin_logout_session()
        #     except Exception as ex:
        #         print("faculty_ajax_faculty_assignment route exception "
        #               "occured>>>>>>>>", ex)
        #
        #
