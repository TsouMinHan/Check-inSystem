from flask import render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, DateField, TextField
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from wtforms.validators import ValidationError, DataRequired, EqualTo
from wtforms.widgets import TextArea

from . import main
from ..models import Student
from app import db, app
import os

class ProfileForm(FlaskForm):
    name = StringField('姓名')
    student_num = StringField("學號")
    photo = FileField('照片')
    password = PasswordField('密碼')
    password2 = PasswordField(
        '確認密碼', validators=[EqualTo('password')])
    father_name = StringField('父親姓名')
    mother_name = StringField('母親姓名')
    class_ = StringField("班級")
    phone_number = IntegerField('連絡電話')
    address = StringField('地址')
    date_of_birth = DateField("生日", format='%Y-%m-%d')
    line_id = StringField('Line ID')

    submit = SubmitField('確認修改')

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()

    # used to display when user requests url.
    data = {
            "name": current_user.name
            , "father_name" : current_user.father_name
            , "mother_name" : current_user.mother_name
            , "phone_number" : current_user.phone_number
            , "address" : current_user.address
            , "class_" : current_user.class_name
            , "student_id" : current_user.student_id
            , "date_of_birth" : current_user.date_of_birth
            , "line_id" : "" if not current_user.line_id else current_user.line_id # SQL return null value if None, so set "".
            }

    if request.method == 'POST' and form.validate_on_submit():
        current_user.phone_number = current_user.phone_number if not form.phone_number.data else form.phone_number.data
        current_user.line_id = current_user.line_id if not form.line_id.data else form.line_id.data

        if form.photo.data:
            f = form.photo.data
            filename = secure_filename(f"{current_user.student_id}.jpg")
            photo_save_path = os.path.join(os.getcwd(), 'app', 'static', 'photos', 'student', filename)
            f.save(photo_save_path)

            current_user.add_face_data(photo_save_path)

        if form.password.data:
            current_user.set_password(form.password.data)
        
        db.session.commit()

        flash("修改資料成功!")

        return redirect(url_for('main.profile'))
    
    return render_template('profile.html', form=form, data=data)