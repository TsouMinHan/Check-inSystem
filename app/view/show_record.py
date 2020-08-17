from flask import render_template, Response
from flask_login import login_required, current_user

from . import main
from ..models import Record


@main.route('/show_record/<student_id>')
@login_required
def show_record_index(student_id):
    data={}
    if current_user.student_id == student_id:
        # show all coll-call record.
        data = Record.get_record(student_id)
    else:
        # show notification tell user did not have right to see record.
        print("not you")
    return render_template('show-record.html', data=data)
    # return render_template('video.html')

    