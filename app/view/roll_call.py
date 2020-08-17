from flask import render_template, redirect, url_for, request, make_response, session, jsonify
from wtforms import SubmitField, SelectField
from flask_login import login_required, current_user
from flask_wtf import FlaskForm

from PIL import Image
import traceback
import datetime
import time
import json
import os
import re

from . import main
from ..models import Record, Student, TakeCourse, Course
from app.recognition import recognize
from ..notify import LineNotify
from .. import audio

global class_dc, end_flog
class_dc = {}
end_flog = False

class RollCallForm(FlaskForm):
    class_name = SelectField('課程', choices=int)
    submit = SubmitField("開始點名")

@main.route("/record_ajax", methods=["POST"])
def record_ajax():
    global class_dc
    data = request.get_json()

    class_name = session["class_name"]
    dc = class_dc[class_name]

    for key, value in dc.items():
        if value["attend"] != data.get(value["student_id"]):
            value["attend"] = not value["attend"]
            value["date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") if value["attend"] else ""
    Record.record(dc)

    session["class_name"] = ""
    del class_dc[class_name]

    return jsonify({"result": "成功送出資料!"})

@main.route("/roll_call", methods=["GET", "POST"])
@login_required
def roll_call_index():
    global class_dc, end_flog

    form = RollCallForm()
    form.class_name.choices = Course.get_course_ls(current_user.teacher_id)

    ## run roll-call
    if form.validate_on_submit():
        
        end_flog = False
        class_dc[form.class_name.data] = Record.create_class_dc(form.class_name.data) 
        recognize.load_data(re.findall(r"(\(.*\))", form.class_name.data)[0][1:-1])

        return redirect(url_for('main.run_roll_call_index', class_=form.class_name.data))
    
    ## end roll-call
    if request.args.get("send"):
        end_flog = True
        class_name = session["class_name"]
        data = class_dc[class_name]
        
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for key, value in data.items():            
            if not data[key]["attend"]:                
                data[key]["date"] = now_time
                Record.record(data[key])
                if data[key].get("line_id"):
                    msg = f"{key} 於 {now_time} {class_name} 課 簽到狀況為 缺席"
                    LineNotify.sendMsg(msg, data[key]["line_id"])  

        session["class_name"] = ""
        del class_dc[class_name]

    return render_template("rollCall.html", form=form)

@main.route("/run_roll_call", methods=["GET", "POST"])
def run_roll_call_index():
    session['class_name'] = request.args.get("class_")
    response = make_response(render_template('run-roll-call.html', title=request.args.get("class_"), mimetype="text/html"))
    return response

@main.route('/image', methods=['POST'])
def image():
    global class_dc, end_flog
    
    if end_flog:
        return
    dc = class_dc[request.form.get('class_name')]

    try:
        image_file = request.files['image']  # get the image

        # Set an image confidence threshold value to limit returned data
        threshold = request.form.get('threshold')

        if threshold is None:
            threshold = 0.5
        else:
            threshold = float(threshold)
        
        # finally run the image through tensor flow object detection`
        image_object = Image.open(image_file)
        
        try:
            objects_ls = recognize.recognition(image_object, dc)
        except Exception as e:
            print(e)
            objects_ls = []

        for ob in objects_ls:
            temp_dc = dc.get(ob.person_name)
            if temp_dc and not temp_dc["attend"]:
                # if it has key of date, don't change data. if not change initial date.
                temp_dc["date"] = temp_dc["date"] if temp_dc["date"] else ob.date

                ob_date = datetime.datetime.strptime(ob.date, "%Y-%m-%d %H:%M:%S")
                dc_date = datetime.datetime.strptime(temp_dc["date"], "%Y-%m-%d %H:%M:%S")

                gap = (ob_date - dc_date).total_seconds()

                if gap >=5 and ob.check_threshold >= gap: # 超過5秒且辨識次數大於秒數
                    temp_dc["date"] = ob.date
                    temp_dc["attend"] = True
                    msg = f"{ob.person_name} 於 {ob.date} 完成 {temp_dc['course_name']} 課 簽到狀況為 出席"
                    
                    Record.record(temp_dc)
                    if temp_dc["line_id"]:
                        LineNotify.sendMsg(msg, temp_dc["line_id"])
                    ob.second = str(gap)
                    temp_dc["second"] = str(gap)

                    ob.student_id = temp_dc["student_id"]

                elif ob.check_threshold < gap: # 辨識次數小於秒數 重新計算
                    temp_dc["date"] = ob.date
                    temp_dc["check_threshold"] = 0
                    temp_dc["second"] = str(0)
                    ob.second = str(0)
                    
                else:
                    temp_dc["check_threshold"] = ob.check_threshold
                    temp_dc["second"] = str(gap)
        
        return json.dumps([ob.__dict__ for ob in objects_ls])

    except Exception as e:
        traceback.print_exc(e)
        o = recognize.Object()
        return json.dumps([o])