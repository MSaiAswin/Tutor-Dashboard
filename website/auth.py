from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/', methods = ['GET', 'POST'])
def verify():
    return render_template('auth/verify.html')


@auth.route('/logout')
def logout():
    return 'Logout'
