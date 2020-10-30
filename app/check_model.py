from api.detection import Detection
from api.facenet import FaceNet,distance
from api.align import AlignDlib

from flask import Blueprint, render_template, Response, redirect, url_for, request,flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from shutil import copyfile

facenet=FaceNet()
facenet.load_weights('models/facenet/nn4.small2.v1.h5')
face=cv2.imread('2face.jpg', 1)[...,::-1]
alignment=AlignDlib('models/align/landmarks.dat')
face_align=alignment.align(96, face, alignment.getLargestFaceBoundingBox(face), landmarkIndices=AlignDlib.OUTER_EYES_AND_NOSE)
if isinstance(face_align,(np.ndarray)):
    print('ok')
    face=face_align
    cv2.imwrite('facealign.jpg', face)
# face = (face / 255.).astype(np.float32)
emb=facenet.make_prediction(face)
print([str(i)+',' for i in emb])