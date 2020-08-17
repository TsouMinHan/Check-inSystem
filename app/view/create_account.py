from flask import render_template, url_for, redirect, request, flash
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, DateField, TextField
from flask_wtf.file import FileField, FileRequired
from flask_login import login_required
from werkzeug.utils import secure_filename
from wtforms.validators import ValidationError, DataRequired, EqualTo
from wtforms.widgets import TextArea

import pandas as pd
import asyncio
import time
import datetime

from . import main
import test
from ..models import Student, TakeCourse
from app import db, app
import os

class ExcelForm(FlaskForm):
    file = FileField("請選擇.xlsx檔案", validators=[FileRequired()])

    submit = SubmitField('確定')

class CreateAccountForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired()])

    father_name = StringField('父親姓名')
    mother_name = StringField('母親姓名')
    class_name = SelectField('班級', choices=int)

    phone_number = IntegerField('連絡電話')
    address = StringField('地址')
    date_of_birth = DateField("生日", format='%Y-%m-%d')

    submit = SubmitField('確定')

@main.route('/create_account', methods=['GET', 'POST'])
@login_required
def create_account_index():
    form = ExcelForm()

    if request.method == 'POST' and form.validate_on_submit():
        file_name = secure_filename(form.file.data.filename)

        if file_name.endswith(".xlsx"):
            file = os.path.join(os.getcwd(), 'app', 'static', 'temp', file_name)
            form.file.data.save(file)

            df = pd.read_excel(file)
            num_of_student = Student.add_student(df)
            
            test.insert_face_data()
            
            flash(f"檔案建立完成，共建立了{num_of_student}個帳號!")

        else:
            flash("檔案格式錯誤，請上傳.xlsx檔案")

        return redirect(url_for('main.create_account_index'))
    
    return render_template('create_account.html', form=form)

@main.route("/create_one_account", methods=["GET", "POST"])
@login_required
def create_one_account_index():
    form = CreateAccountForm()
    form.class_name.choices = Student.get_all_class()

    if form.validate_on_submit():
        temp_student_id = Student.query.filter_by(class_name=form.class_name.data).order_by(Student.student_id.desc()).first().student_id

        temp_student_id = int(temp_student_id) + 1

        user = Student(name=form.name.data
                , father_name=form.father_name.data
                , mother_name=form.mother_name.data
                , phone_number=form.phone_number.data
                , address=form.address.data
                , class_name=form.class_name.data
                , date_of_birth=form.date_of_birth.data
                , student_id=temp_student_id
                )
        
        user.set_password(user.date_of_birth.strftime("%Y%m%d"))

        TakeCourse.create_course(form.class_name.data, temp_student_id)
                
        db.session.add(user)
        db.session.commit()

        flash(f"帳號建立完成")

        return redirect(url_for('main.create_one_account_index'))
    return render_template('create_one_account.html', form=form)