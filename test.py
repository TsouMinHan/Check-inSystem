from app import db
from app.models import Student, Course, Teacher, TakeCourse
from os import listdir, rename
from os.path import isfile, join
import tempfile
from gtts import gTTS

def file_rename():
    path = "D:\\pyCharm\\Check-inSystem\\app\\static\\photo"
    num_ls = [31,33,36]
    class_ls = ["01", "02", "03"]
    pre_txt = "10902"

    for i, f in enumerate(listdir(path)):
        if i <31:
            student_id = f"{pre_txt}{class_ls[0]}{str(i+1).zfill(2)}"
        elif i<64:
            student_id = f"{pre_txt}{class_ls[1]}{str(i-31+1).zfill(2)}"
        else:
            student_id = f"{pre_txt}{class_ls[2]}{str(i-64+1).zfill(2)}"

        rename(f"{path}\\{f}", f"{path}\\{student_id}.jpg")

def insert_face_data():
    # get all Student
    student_ls = Student.query.all()

    path = "D:\\pyCharm\\Check-inSystem\\app\\static\\photos\\student"

    # add facedata
    for i, s in enumerate(student_ls):
        print(f"{path}\\{s.student_id}", s.name)
        if not s.face_data:
            s.add_face_data(f"{path}\\{s.student_id}.jpg")

def add_course():
    Course.add_course("D:/pyCharm/Check-inSystem/app/static/doc/course.xlsx")

def add_teacher_info():
    t = Teacher(
        name="教師",
        teacher_id="AB0001",
        phone_number="09123321123"
    )
    t.set_password("123")
    db.session.add(t)
    db.session.commit()

def generate_audio_file():
    student_ls = Student.query.all()
    for s in student_ls:

        with tempfile.NamedTemporaryFile(delete=True) as fp:
            tts = gTTS(text=f"{s.name}以完成點名", lang='zh-TW')
            filename = fp.name.split("\\")[-1]
            tts.save(f"./app/static/audio/{s.student_id}.mp3")

if __name__ == "__main__":
    generate_audio_file()
    pass