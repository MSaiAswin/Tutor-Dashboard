from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/', methods = ['GET', 'POST'])
def verify():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged In!', category = 'success')
                login_user(user, remember = True)
                return redirect(url_for('views.home'))

            else:
                flash('Password is Incorrect!', category = 'error')
        else:
            flash('User does not Exist!', category = 'error')

        # user = User(email = email, password = generate_password_hash(password, method = 'sha256'), name = 'Sai Aswin')
        # db.session.add(user)
        # db.session.commit()

        # user = User.query.filter_by(name = 'Sai Aswin').first()
        # print([user.id, user.email, user.name, user.password])





    return render_template('auth/verify.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out!', category='success')
    return redirect(url_for('auth.verify'))
