from flask import redirect, url_for, render_template, request, flash
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app.models import Student, Teacher
from . import main


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length

class LoginForm(FlaskForm):
    name = StringField('帳號', validators=[DataRequired()])
    password = PasswordField('密碼（預設為生日 例：19900916）', validators=[DataRequired()])
    identity = SelectField('身份', choices=[("student", "學生"), ("teacher", '教師')])
    remember_me = BooleanField('記住登入資訊')
    submit = SubmitField('登入')

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('.index'))

    form = LoginForm()

    if form.validate_on_submit():
        if form.identity.data == "teacher":
            user = Teacher.query.filter_by(teacher_id=form.name.data).first()

        elif form.identity.data == "student":
            user = Student.query.filter_by(student_id=form.name.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('錯誤的帳號或密碼')
            return redirect(url_for('main.login'))

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')

        return redirect(next_page)
        
    return render_template('login.html', form=form)