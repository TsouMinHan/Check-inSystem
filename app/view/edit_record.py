from flask import render_template, Response, redirect, url_for, session, request, jsonify
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length

from . import main
from ..models import Record
from ..notify import LineNotify

class SearchForm(FlaskForm):
    student_id = StringField('學號')

    submit = SubmitField('搜尋')

@main.route('/edit_record', methods=["GET", "POST"])
@login_required
def edit_record_index():
    form = SearchForm()
    data = {}

    if form.validate_on_submit():
        student_id = form.student_id.data
        data = Record.get_record(student_id)

    return render_template('edit-record.html', data=data, form=form)
    # return render_template('video.html')

@main.route("/edit_record_ajax", methods=["POST"])
def edit_record_ajax():
    data = request.get_json()
    student_id, date, checked, course_name, student_name = data["student_id"], data["date"], data["checked"], data["course_name"], data["student_name"]
    line_id = Record.edit_record(student_id, date, checked)
    m = "出席" if checked else "曠課"

    LineNotify.sendMsg(f"修改 {student_name} 於 {date} {course_name} 課的點名記錄為 {m}", line_id)

    return jsonify({"result": "成功修改資料!"})
