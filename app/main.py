# main.py

from flask import Blueprint, render_template,request,redirect
from flask_login import login_required, current_user
from api.emotions import EmotionDetector
from api.detection import Detection
import cv2
import datetime
from .models import ShopLists, Status
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')



@main.route('/add', methods=['POST'])
def add_task():
    content = request.form['content']
    if not content:
        return 'Error'

    product = ShopLists(current_user.id,content)
    db.session.add(product)
    db.session.commit()
    return redirect('/lista')


@main.route('/delete/<int:id_product>')
def delete_product(id_product):
    product = ShopLists.query.get(id_product)
    if not product:
        return redirect('/lista')

    db.session.delete(product)
    db.session.commit()
    return redirect('/lista')

@main.route('/lista')
@login_required
def lista():
    shopList = ShopLists.query.get(current_user.id)
    shopList = db.session.query(ShopLists).filter_by(id_user = current_user.id).all()
    print(shopList)
    return render_template('list.html',shopList=shopList)
# shopList = db.session.query(ShopLists).filter_by(id_user = current_user.id).one()


@main.route('/profile')
@login_required
def profile():
    #get photo
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        if  ret:
            break
    cam.release()
    #get face
    detectFace=Detection()
    faces=detectFace.find_faces(frame)
    if len(faces)>=1:
        face=faces[0][1]
        # cv2.imwrite('iin.jpg',face)
        # image=cv2.imread('face.jpg')
        #get emotion
        gray_image = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        emotion_recognition=EmotionDetector()
        emotion_recognition.load_model('models/emotions/fer2013_mini_XCEPTION.102-0.66.hdf5')
        color=emotion_recognition.make_prediction(gray_image)
        #add to DB
        status = Status(current_user.id,color,datetime.datetime.utcnow())
        db.session.add(status)
        db.session.commit()
        print(color)
    else:
        color=None
    #path to img
    pathToImg='https://faceverificationphotos.s3.eu-central-1.amazonaws.com/'+current_user.link+'/face.jpg'
    # print(pathToImg2)
    # pathToImg='../mgr_faceid/'+current_user.email+'/face.jpg'
    return render_template('profile.html',name=current_user.name,color=color,pathToImg=pathToImg)