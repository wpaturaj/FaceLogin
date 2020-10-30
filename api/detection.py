from mtcnn.mtcnn import MTCNN
import cv2
from scipy import misc
import numpy as np

class Detection:
    # face detection parameters
    def __init__(self, face_crop_size=160, face_crop_margin=60):
        self.detector=MTCNN()
        self.face_crop_size = face_crop_size
        self.face_crop_margin = face_crop_margin

    def find_faces(self, image):
        faces = []
        bounding_boxes = self.detector.detect_faces(image)
        for res in bounding_boxes:
            face=[]
            bb = res['box']
            bounding_box_new = np.zeros(4, dtype=np.int32)
            img_size = np.asarray(image.shape)[0:2]
            bounding_box_new[0] = np.maximum(bb[0] - self.face_crop_margin / 2, 0)
            bounding_box_new[1] = np.maximum(bb[1] - self.face_crop_margin / 2, 0)
            bounding_box_new[2] = np.minimum(bb[2]+bb[0] + self.face_crop_margin / 2, img_size[1])
            bounding_box_new[3] = np.minimum(bb[3]+bb[1] + self.face_crop_margin / 2, img_size[0])
            cropped = image[bounding_box_new[1]:bounding_box_new[3], bounding_box_new[0]:bounding_box_new[2], :]
            fimage = misc.imresize(cropped, (self.face_crop_size, self.face_crop_size), interp='bilinear')
            face.append(image)
            face.append(fimage)
            faces.append(face)
        return faces