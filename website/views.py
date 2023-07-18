from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Student, Batch, User, Alumini
from . import db
from datetime import date
import datetime

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






###########   Batch Management Related Views   ########################



@views.route('/batch')
@login_required
def batch():
    return render_template('batch/batch.html')

@views.route('/batch/add', methods=['GET', 'POST'])
@login_required
def addBatch():



    if request.method == 'POST' and request.form.get('submit') == 'new':

        name = request.form.get('name')
        days = {
                'sunday' : createTime(request.form.get('sunday')),
                'monday' : createTime(request.form.get('monday')),
                'tuesday' : createTime(request.form.get('tuesday')),
                'wednesday' : createTime(request.form.get('wednesday')),
                'thursday' : createTime(request.form.get('thursday')),
                'friday' : createTime(request.form.get('friday')),
                'saturday' : createTime(request.form.get('saturday'))
                }


        batch_exists = Batch.query.filter_by(name=name).first()
        batches = Batch.query.all()

        for day in days:
            for batch in batches:
                if day == 'sunday' and batch.sunday != None and days[day] != datetime.time():
                    if (days[day] <= batch.sunday < datetime.time(days[day].hour+1,days[day].minute)) or (batch.sunday <= days[day] < datetime.time(batch.sunday.hour+1,batch.sunday.minute)):
                        flas = f'Batch coincides with {batch.name} on {day} at {batch.sunday}'
                        flash(flas, category='error')
                        return redirect(url_for('views.addBatch'))

                if day == 'monday' and batch.monday != None and days[day] != datetime.time():
                    if (days[day] <= batch.monday < datetime.time(days[day].hour+1,days[day].minute)) or (batch.monday <= days[day] < datetime.time(batch.monday.hour+1,batch.sunday.minute)):
                        flas = f'Batch coincides with {batch.name} on {day} at {batch.monday}'
                        flash(flas, category='error')
                        return redirect(url_for('views.addBatch'))

                if day == 'tuesday' and batch.tuesday != None and days[day] != datetime.time():
                    if (days[day] <= batch.tuesday < datetime.time(days[day].hour+1,days[day].minute)) or (batch.tuesday <= days[day] < datetime.time(batch.tuesday.hour+1,batch.sunday.minute)):
                        flas = f'Batch coincides with {batch.name} on {day} at {batch.tuesday}'
                        flash(flas, category='error')
                        return redirect(url_for('views.addBatch'))

                if day == 'wednesday' and batch.wednesday != None and days[day] != datetime.time():
                    if (days[day] <= batch.wednesday < datetime.time(days[day].hour+1,days[day].minute)) or (batch.wednesday <= days[day] < datetime.time(batch.wednesday.hour+1,batch.sunday.minute)):
                        flas = f'Batch coincides with {batch.name} on {day} at {batch.wednesday}'
                        flash(flas, category='error')
                        return redirect(url_for('views.addBatch'))

                if day == 'thursday' and batch.thursday != None and days[day] != datetime.time():
                    if (days[day] <= batch.thursday < datetime.time(days[day].hour+1,days[day].minute)) or (batch.thursday <= days[day] < datetime.time(batch.thursday.hour+1,batch.sunday.minute)):
                        flas = f'Batch coincides with {batch.name} on {day} at {batch.thursday}'
                        flash(flas, category='error')
                        return redirect(url_for('views.addBatch'))

                if day == 'friday' and batch.friday != None and days[day] != datetime.time():
                    if (days[day] <= batch.friday < datetime.time(days[day].hour+1,days[day].minute)) or (batch.friday <= days[day] < datetime.time(batch.friday.hour+1,batch.sunday.minute)):
                        flas = f'Batch coincides with {batch.name} on {day} at {batch.friday}'
                        flash(flas, category='error')
                        return redirect(url_for('views.addBatch'))

                if day == 'saturday' and batch.saturday != None and days[day] != datetime.time():
                    if (days[day] <= batch.saturday < datetime.time(days[day].hour+1,days[day].minute)) or (batch.saturday <= days[day] < datetime.time(batch.saturday.hour+1,batch.sunday.minute)):
                        flas = f'Batch coincides with {batch.name} on {day} at {batch.saturday}'
                        flash(flas, category='error')
                        return redirect(url_for('views.addBatch'))




        if batch_exists :
            flash('Batch Already Exists!', category='error')
        else:

            # print(saturday+' '+type(saturday))
            batch = Batch(name=name, sunday=days['sunday'], monday=days['monday'], tuesday=days['tuesday'], wednesday=days['wednesday'], thursday=days['thursday'], friday=days['friday'], saturday=days['saturday'])
            db.session.add(batch)
            db.session.commit()
            flash('Batch Added!', category='success')
            return redirect(url_for('views.batch'))

    return render_template('batch/add.html')

def createTime(timeString):
    if timeString:
        try:
            time = datetime.datetime.strptime(timeString,'%H:%M').time()
        except:
            time = datetime.datetime.strptime(timeString,'%H:%M:%S').time()
    else:
        time = datetime.datetime.strptime(timeString,'').time()

    return time



@views.route('/batch/remove', methods=['GET', 'POST'])
@login_required
def removeBatch():

    if request.method == 'POST' and request.form.get('submit') == 'select':
        id = int(request.form.get('name'))
        batch = Batch.query.get(id)
        return render_template('batch/remove.html', batch = batch, time = datetime.time())

    if request.method == 'POST' and request.form.get('submit') == 'remove':
        id = int(request.form.get('confirm'))
        batch = Batch.query.get(id)
        db.session.delete(batch)
        db.session.commit()
        flash('Batch Deleted!', category='success')
        return redirect(url_for('views.batch'))

    batches = Batch.query.all()
    return render_template('batch/select.html', batches = batches)


@views.route('/batch/edit', methods=['GET', 'POST'])
@login_required
def editBatch():

    if request.method == 'POST' and request.form.get('submit') == 'select':
        id = int(request.form.get('name'))
        batch = Batch.query.get(id)
        return render_template('batch/edit.html', batch=batch, time=datetime.time())

    if request.method == 'POST' and request.form.get('submit') == 'edit':
        id = int(request.form.get('id'))
        batch = Batch.query.get(id)

        batch.name = request.form.get('name')
        batch.sunday = createTime(request.form.get('sunday'))
        batch.monday = createTime(request.form.get('monday'))
        batch.tuesday = createTime(request.form.get('tuesday'))
        batch.wednesday = createTime(request.form.get('wednesday'))
        batch.thursday = createTime(request.form.get('thursday'))
        batch.friday = createTime(request.form.get('friday'))
        batch.saturday = createTime(request.form.get('saturday'))


        db.session.commit()
        flash('Batch Edited!', category = 'success')
        return redirect(url_for('views.batch'))

    batches = Batch.query.all()
    return render_template('batch/select.html', batches = batches)


@views.route('/batch/view', methods=['GET', 'POST'])
@login_required
def viewBatch():

    if request.method == 'POST' and request.form.get('submit') == 'select':
        id = int(request.form.get('name'))
        batch = Batch.query.get(id)
        return render_template('batch/view.html', batch=batch, time=datetime.time())


    batches = Batch.query.all()
    return render_template('batch/select.html', batches = batches)

########################################################################
