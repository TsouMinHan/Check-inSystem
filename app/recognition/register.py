import dlib
import numpy as np
import cv2
import os
import json

detector = dlib.cnn_face_detection_model_v1('./app/static/doc/mmod_human_face_detector.dat')
# detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('./app/static/doc/shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('./app/static/doc/dlib_face_recognition_resnet_model_v1.dat')

def get_face_data(image_path):
    data = np.zeros((1,128))
    label = []

    fileName = image_path
    # labelName = file.split('_')[0]
    # print('current image: ', file)
    # print('current label: ', labelName)
    
    img = cv2.imread(image_path)

    while img.shape[0]*img.shape[1] > 500000:
        img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)

    dets = detector(img, 1)

    for k, d in enumerate(dets):
        rec = dlib.rectangle(d.rect.left(), d.rect.top(), d.rect.right(), d.rect.bottom())
        shape = sp(img, rec)
        face_descriptor = facerec.compute_face_descriptor(img, shape)
        faceArray = np.array(face_descriptor).reshape((1, 128))
        data = np.concatenate((data, faceArray))
    data = data[1:, :][0]
    
    return np.array2string(data, precision=10, separator=' ', suppress_small=True)[1:-1].replace("\n", "")


if __name__ == '__main__':
    image_path = r'D:\\pyCharm\\Check-inSystem\\app\\static\\img\\1_1.png'
    a = get_face_data(image_path)
    print(type(a))
    print(a)
