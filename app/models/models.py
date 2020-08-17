from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

import numpy as np
import sqlite3
import asyncio
import pandas as pd

from app.recognition import register
from app import login
from app import db

@login.user_loader
def load_user(id):
    _id = id.split("-")[0]
    table_name = id.split("-")[1]
    
    if table_name == "Teacher":
        return Teacher.query.get(int(_id))
    elif table_name == "Student":
        return Student.query.get(int(_id))

class Teacher(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    teacher_id = db.Column(db.String(6))
    password_hash = db.Column(db.String(128))
    phone_number = db.Column(db.String(10))

    def __repr__(self):
        return f'<User {self.name}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id) + "-" + "Teacher"

    def get_table_name(self):
        return "Teacher"

class Student(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    father_name = db.Column(db.String(10))
    mother_name = db.Column(db.String(10))

    password_hash = db.Column(db.String(128))
    phone_number = db.Column(db.String(10))
    address = db.Column(db.String(32))
    class_name = db.Column(db.String(10))
    student_id = db.Column(db.String(9))
    date_of_birth = db.Column(db.String(10))
    line_id = db.Column(db.String(64))
    face_data = db.Column(db.Text)

    def __repr__(self):
        return f'<User {self.name}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def add_face_data(self, photo_save_path):
        self.face_data = register.get_face_data(photo_save_path)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)   

    def get_id(self):
        return str(self.id) + "-" + "Student"

    def get_table_name(self):
        return "Student"

    @classmethod
    def get_all_class(cls) -> list:
        class_ = db.session.query(cls.class_name).all()
        ls = []
        for c in class_:
            if c[0] not in ls:
                ls.append(c[0])
        return [ (c, c) for c in ls ]

    @classmethod
    def get_face_data_ls_and_name_ls(cls, class_name) -> list:
        face_data_ls = []
        name_ls = []
        for ele in cls.query.filter_by(class_name=class_name).all():
            if ele.face_data:
                face_data_ls.append(ele.face_data)
                name_ls.append(ele.name)
        
        return "\n".join(face_data_ls), name_ls    

    @classmethod
    def add_student(cls, data):
        for i in range(data.shape[0]):
            person = data.iloc[i]
            
            user = Student(name=person["姓名"]
                        , father_name=person["父親"]
                        , mother_name=person["母親"]
                        , phone_number=str(person["連絡電話"]).zfill(10)
                        , address=person["地址"]
                        , class_name=person["班級"]
                        , date_of_birth=person["生日"].strftime("%Y-%m-%d")
                        , student_id=str(person["學號"])
                        )
            user.set_password(person["生日"].strftime("%Y%m%d"))

            TakeCourse.create_course(person["班級"], str(person["學號"]))

            db.session.add(user)
        db.session.commit()

        return data.shape[0]

    @classmethod
    def get_class_member(cls, class_name):
        return cls.query.filter_by(class_name=class_name).all()

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(4))
    student_id = db.Column(db.String(9))

    date = db.Column(db.String(10))
    attend = db.Column(db.Boolean, default=False)

    @classmethod
    def create_class_dc(cls, course_name, class_name=""):
        dc = {}

        if class_name:
            student_ls = Student.query.filter_by(class_name=class_name).all()
    
            for s in student_ls:
                dc[s.name] = {
                                    "course_name": course_name,
                                    "course_id": course_name,
                                    "student_id": s.student_id,
                                    "date": None,
                                    "attend": False,
                                    "check_threshold": 0,
                                    "line_id": s.line_id,
                                    "second": "0"
                                }

        else:
            course_id = Course.query.filter_by(course_name=course_name).first().course_id
            student_ls = TakeCourse.query.filter_by(course_id=course_id).all()

            for s in student_ls:
                student_name = Student.query.filter_by(student_id=s.student_id).first().name
                dc[student_name] = {
                                    "course_name": course_name,
                                    "course_id": course_id,
                                    "student_id": s.student_id,
                                    "date": None,
                                    "attend": False,
                                    "check_threshold": 0,
                                    "line_id": Student.query.filter_by(student_id=s.student_id).first().line_id,
                                    "second": "0"
                                }
        

        
        return dc

    @classmethod
    def record(cls, dc):

        rec = Record(
                    course_id=dc["course_id"],
                    student_id=dc["student_id"],
                    date=dc["date"],
                    attend=dc["attend"]
                )

        db.session.add(rec)
        db.session.commit()

    @classmethod
    def get_record(cls, student_id):
        record_ls = cls.query.filter_by(student_id=student_id).order_by(cls.date.desc())
        dc = {}
        student = Student.query.filter_by(student_id=student_id)[0]

        for i, ele in enumerate(record_ls):
            course_name = Course.query.filter_by(course_id=ele.course_id).first().course_name
            dc[i] = {
                "attend": ele.attend,
                "course_name": course_name,
                "date": ele.date,
                "student_name": student.name,
                "class_name": student.class_name,
                "student_id": student_id
            }
        return dc

    @classmethod
    def edit_record(cls, student_id, date, checked):
        record = cls.query.filter_by(student_id=student_id, date=date).first()
        record.attend = checked

        db.session.commit()

        return Student.query.filter_by(student_id=student_id).first().line_id

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(4))
    course_name = db.Column(db.String(10))

    teacher_id = db.Column(db.String(6))

    @classmethod
    def add_course(cls, file):
        df = pd.read_excel(file)
        row_num = df.shape[0]
        
        for i in range(row_num):
            course = df.iloc[i]
            
            c = cls(course_id=course["編號"],
                       course_name=course["名稱"],
                       teacher_id=course["教師"])
            
            db.session.add(c)
        db.session.commit()

    @classmethod
    def get_course_ls(cls, teacher_id):
        res = db.session.query(cls.course_name).filter_by(teacher_id=teacher_id).all()
        return [(cl[0], cl[0]) for cl in res] # res = [("class", ), ("class", )]

    @classmethod
    def create_course(cls, course_name, teacher_id, class_name):
        course_id = cls.query.order_by(cls.course_id.desc()).first().course_id
        course_id = "A" + str(int(course_id[1:])+1).zfill(3)
        c = cls(
            course_id=course_id,
            course_name=f"({class_name}){course_name}",
            teacher_id=teacher_id
        )
        db.session.add(c)
        db.session.commit()

        return course_id

class TakeCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(4))    
    student_id = db.Column(db.String(9))

    @classmethod
    def create_course(cls, class_name, student_id):    
        if class_name == "二年一班":
            course_id = ["A001", "A004","A007"]

        elif class_name == "二年二班":
            course_id = ["A002", "A005","A008"]

        elif class_name == "二年三班":
            course_id = ["A003", "A006","A009"]

        for i in course_id:
            c = cls(
                course_id=i,
                student_id=student_id
            )

            db.session.add(c)
        db.session.commit()

    @classmethod
    def creat_new_course(cls,course_id, student_id):
        c = cls(
            course_id=course_id,
            student_id=student_id
        )

        db.session.add(c)
        db.session.commit()


if __name__ == "__main__":
    pass

