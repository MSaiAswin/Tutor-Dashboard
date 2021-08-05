from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Student, Batch, User, Alumini
from . import db
from datetime import date

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
@login_required
def home():
    return render_template('home.html', name = current_user.name)

@views.route('/test')
@login_required
def test():
    return render_template('student/test.html')


##########   Student Management Related Views   #######################

@views.route('/student')
@login_required
def student():
    return render_template('student/student.html')



@views.route('/student/add', methods=['GET', 'POST'])
@login_required
def addStud():
    if request.method == 'POST' and request.form.get('choice'):
        choice = request.form.get('choice')
        if choice == 'old':
            batches = Batch.query.all()
            aluminis = Alumini.query.all()
            return render_template('student/addOld.html', batches=batches, aluminis=aluminis)
        elif choice == 'new':
            batches = Batch.query.all()
            return render_template('student/addNew.html', batches=batches)

    if request.method == 'POST' and request.form.get('submit') == 'new':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        school = request.form.get('school')
        dob = request.form.get('dob')
        batch = request.form.get('batch')

        batch_object = Batch.query.filter_by(name=batch).first()
        dob = date.fromisoformat(dob)

        student_exists = Student.query.filter_by(name=name).first()

        if student_exists and student_exists.dob == dob:
            flash('Student Already Exists!', category='error')
        else:

            student = Student(name=name, phone=phone, email=email, school=school, dob=dob, batch=batch_object)
            db.session.add(student)
            db.session.commit()
            flash('Student Added!', category='success')
            return redirect(url_for('views.student'))

    elif request.method == 'POST' and request.form.get('submit') == 'old':
        id = int(request.form.get('name'))
        batch = request.form.get('batch')

        batch_object = Batch.query.filter_by(name=batch).first()

        alumini = Alumini.query.get(id)
        student = Student(name=alumini.name, phone=alumini.phone, email=alumini.email, school=alumini.school, dob=alumini.dob, batch=batch_object)

        db.session.add(student)
        db.session.delete(alumini)
        db.session.commit()
        flash('Student Added!', category='success')
        return redirect(url_for('views.student'))

    return render_template('student/add.html')



@views.route('/student/remove', methods=['GET', 'POST'])
@login_required
def removeStud():

    if request.method == 'POST' and request.form.get('submit') == 'select':
        id = int(request.form.get('name'))
        student = Student.query.get(id)
        return render_template('student/remove.html', student = student)

    if request.method == 'POST' and request.form.get('confirm_name'):
        id = int(request.form.get('confirm_name'))
        student = Student.query.get(id)
        alumini = Alumini(name=student.name, phone=student.phone, email=student.email, school=student.school, dob=student.dob)
        db.session.add(alumini)
        db.session.delete(student)
        db.session.commit()
        flash('Student Deleted!', category='success')
        return redirect(url_for('views.student'))

    students = Student.query.all()
    return render_template('student/select.html', students=students)



@views.route('/student/edit', methods=['GET', 'POST'])
@login_required
def editStud():

    if request.method == 'POST' and request.form.get('submit') == 'select':
        id = int(request.form.get('name'))
        student = Student.query.get(id)
        batch = student.batch.name
        batches = Batch.query.all()
        return render_template('student/edit.html', student = student, batch=batch, batches = batches)

    if request.method == 'POST' and request.form.get('submit') == 'edit':
        id = int(request.form.get('id'))
        student = Student.query.get(id)
        batch = request.form.get('batch')
        batch_object = Batch.query.filter_by(name=batch).first()

        student.name = request.form.get('name')
        student.phone = request.form.get('phone')
        student.email = request.form.get('email')
        student.school = request.form.get('school')
        student.dob = date.fromisoformat(request.form.get('dob'))
        student.batch_id = batch_object.id

        db.session.commit()
        flash('Student Edited!', category = 'success')
        return redirect(url_for('views.student'))

    students = Student.query.all()
    return render_template('student/select.html', students=students)

@views.route('/student/view', methods=['GET', 'POST'])
@login_required
def viewStud():

    if request.method == 'POST' and request.form.get('submit') == 'select':
        id = int(request.form.get('name'))
        student = Student.query.get(id)
        batch = student.batch.name
        return render_template('student/view.html', student = student, batch=batch)

    students = Student.query.all()
    return render_template('student/select.html', students=students)
#######################################################################
