# auth.py

from flask import Blueprint, render_template, Response, redirect, url_for, request,flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from shutil import copyfile
from .models import User
from . import db
import cv2
import os
import numpy as np
import boto3
from botocore.client import Config
from io import BytesIO
import matplotlib.image as mpimg
from api.detection import Detection
from api.facenet import FaceNet,distance
from api.align import AlignDlib
import hashlib
from PIL import Image
from .utils import *

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    # usuwamy aktualne zdjecie z pamiieci
    if os.path.exists("face.jpg"):
        os.remove("face.jpg")
    return render_template('login.html')
    
@auth.route('/login', methods=['POST'])
def login_post():
    # uzupelniamy formularz oraz wczytujemy modele predykcyjne
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()

    #FaceNet
    facenet=FaceNet()
    facenet.load_weights('models/facenet/nn4.small2.v1.h5')
    face=cv2.imread('face.jpg', 1)[...,::-1]
    alignment=AlignDlib('models/align/landmarks.dat')
    face_align=alignment.align(96, face, alignment.getLargestFaceBoundingBox(face), landmarkIndices=AlignDlib.OUTER_EYES_AND_NOSE)
    if isinstance(face_align,(np.ndarray)):
        print('ok')
        face=face_align
        cv2.imwrite('facealign.jpg', face)
    # face = (face / 255.).astype(np.float32)
    emb=facenet.make_prediction(face)
    print([str(i)+',' for i in emb])    # check if user actually existsS
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password): 
        flash('Niepoprawny login lub haslo')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page
    # face verification
    print(distance(np.array(emb),np.array(user.embeeding)))
    if distance(np.array(emb),np.array(user.embeeding))>0.85:
        flash('Przykro Nam, ale nie mozemy uwierzytelnic Twojego konta')
        return redirect(url_for('auth.login')) 
    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.lista'))

def gen():
    vc = cv2.VideoCapture(0)
    detectFace=Detection()
    while True:
        cv2.waitKey(800)
        rval, frame = vc.read()
        nowe=detectFace.find_faces(frame)
        if len(nowe)==1:
            frame=nowe[0][0]
            # k = cv2.waitKey(33)
            # if k==27:    # Esc key to stop
            #     break
            cv2.imwrite('face.jpg', nowe[0][1])
            yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('face.jpg', 'rb').read() + b'\r\n') 
            break
        cv2.imwrite('t.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n') 
 


@auth.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@auth.route('/signup')
def signup():
    if os.path.exists("face.jpg"):
        os.remove("face.jpg")
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
    if user: # if a user is found, we want to redirect back to signup page so user can try again
    	flash('Konto o podanym adresie juz istnieje.')
    	return redirect(url_for('auth.signup'))
    #FaceNet
    facenet=FaceNet()
    facenet.load_weights('models/facenet/nn4.small2.v1.h5')
    face=cv2.imread('face.jpg', 1)[...,::-1]
    alignment=AlignDlib('models/align/landmarks.dat')
    face_align=alignment.align(96, face, alignment.getLargestFaceBoundingBox(face), landmarkIndices=AlignDlib.OUTER_EYES_AND_NOSE)
    if isinstance(face_align,(np.ndarray)):
        print('ok')
        face=face_align
        cv2.imwrite('2face.jpg', face)
    # face = (face / 255.).astype(np.float32)
    emb=facenet.make_prediction(face)
    #addUser
    hashEmail=hashEmailAddress(email)
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'),embeeding=list(emb),link=hashEmail)
    db.session.add(new_user)
    db.session.commit()
    #try
    filePath=hashEmail+"/face.jpg"
    data = open('face.jpg', 'rb')
    # cv2.imwrite('face3.jpg', data)
    print(filePath)
    uploadFileS3(data,filePath,ACCESS_KEY_ID,ACCESS_SECRET_KEY,BUCKET_NAME)
    return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))