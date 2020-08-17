from flask import render_template, redirect, url_for, flash
from wtforms.validators import ValidationError, DataRequired
from wtforms import SubmitField, SelectField, StringField
from flask_login import login_required, current_user
from flask_wtf import FlaskForm

from . import main
from ..models import Record, Student, TakeCourse, Course

class RollCallForm(FlaskForm):
    course_name = StringField('課程名稱')
    class_name = SelectField('班級', choices=int)
    submit = SubmitField("建立課程")

@main.route("/create_course", methods=["GET", "POST"])
@login_required
def create_course_index():
    form = RollCallForm()
    form.class_name.choices = Student.get_all_class()

    if form.validate_on_submit():
        course_name = form.course_name.data
        class_name = form.class_name.data

        course_id = Course.create_course(course_name, current_user.teacher_id, class_name)
        student_ls = Student.get_class_member(class_name)

        for s in student_ls:
            TakeCourse.creat_new_course(course_id, s.student_id)
        flash(f"課程建立完成")
    return render_template("create-course.html", form=form)