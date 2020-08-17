import dlib
import numpy as np
import cv2
import json
import datetime

from ..models import Student
from io import StringIO

class Object(object):
    def __init__(self):
        self.person_name = ""
        self.x = ""
        self.y = ""
        self.height = ""
        self.width = ""
        self.attend = False
        self.check_threshold = 0
        self.date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.second = "0"
        self.student_id = ""

    def toJSON(self):
        return json.dumps(self.__dict__)

detector = dlib.cnn_face_detection_model_v1('./app/static/doc/mmod_human_face_detector.dat')
# detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('./app/static/doc/shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('./app/static/doc/dlib_face_recognition_resnet_model_v1.dat')
threshold = 0.48

other_label = "other"


def load_data(class_name):
    global data, label_ls
    data, label_ls = Student.get_face_data_ls_and_name_ls(class_name)
    try:
        data = np.loadtxt(StringIO(data), dtype=float)
    except:
        pass

def findNearestClassForImage(face_descriptor, faceLabel):
    global data
    temp =  face_descriptor - data
    try:
        e = np.linalg.norm(temp,axis=1,keepdims=True)
    except:
        e = np.linalg.norm(temp,axis=0,keepdims=True)

    min_distance = e.min() 
    print('distance: ', min_distance)
    if min_distance > threshold:
        return other_label
    try:
        index = np.argmin(e)
        return faceLabel[index]
    except:
        return other_label

# for HOG
# def recognition(image_path, dc={}):
#     global label_ls
#     output = []

#     img = cv2.cvtColor(np.asarray(image_path),cv2.COLOR_RGB2BGR)
#     shrink_times = 1
#     while img.shape[0]*img.shape[1] > 500000:
#         shrink_times +=1
#         img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)

#     dets = detector(img, 1)

#     for k, d in enumerate(dets):
#         rec = dlib.rectangle(d.left(),d.top(),d.right(),d.bottom())

#         shape = sp(img, rec)
#         face_descriptor = facerec.compute_face_descriptor(img, shape)        
        
#         class_pre = findNearestClassForImage(face_descriptor, label_ls)

#         shrink = 3**(shrink_times-2)

#         item = Object()

#         item.person_name = class_pre
#         item.y = rec.top()*shrink
#         item.x = rec.left()*shrink
#         item.height = rec.bottom()*shrink
#         item.width = rec.right()*shrink
#         if class_pre != other_label:
#             item.check_threshold = dc[class_pre]["check_threshold"] + 1
#             item.second = dc[class_pre]["second"]
            
#         output.append(item)
        
    

#     return output

def recognition(image_path, dc={}):
    global label_ls
    output = []

    img = cv2.cvtColor(np.asarray(image_path),cv2.COLOR_RGB2BGR)
    shrink_times = 1
    while img.shape[0]*img.shape[1] > 500000:
        shrink_times +=1
        img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)

    dets = detector(img, 1)

    for k, d in enumerate(dets):
        rec = dlib.rectangle(d.rect.left(),d.rect.top(),d.rect.right(),d.rect.bottom())

        shape = sp(img, rec)
        face_descriptor = facerec.compute_face_descriptor(img, shape)        
        
        class_pre = findNearestClassForImage(face_descriptor, label_ls)
        print(class_pre)
        shrink = 3**(shrink_times-2)

        item = Object()

        item.person_name = class_pre
        item.y = rec.top()*shrink
        item.x = rec.left()*shrink
        item.height = rec.bottom()*shrink
        item.width = rec.right()*shrink
        if class_pre != other_label:
            item.check_threshold = dc[class_pre]["check_threshold"] + 1
            item.second = dc[class_pre]["second"]
            
        output.append(item)
    return output
    
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    fps = 10
    size = (640,480)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # videoWriter = cv2.VideoWriter('video.MP4', fourcc, fps, size)

    while(1):
        ret, frame = cap.read()
        #frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
        recognition(frame)
        # videoWriter.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    # videoWriter.release()
    cv2.destroyAllWindows()    