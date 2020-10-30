import cv2
from keras.models import load_model
import numpy as np

class EmotionDetector():
    def __init__(self):
        self.model=None
        self.shape_to_resize=None
        self.color_map={0: "#FF1744",
         1: "#cdcdff",
         2: '#4c0000',
         3: "#4ca64c",
         4: "#9999ff",
         5: "#e5e500",
         6: "#cccccc"}
    def load_model(self,path_to_model):
        try:
            self.model = load_model(path_to_model, compile=False)
            self.shape_to_resize=self.model.input_shape[1:3]
        except Exception as e:
            return e
    def preprocess_input(self,x, v2=True):
        x = x.astype('float32')
        x = x / 255.0
        if v2:
            x = x - 0.5
            x = x * 2.0
        return x
    def make_prediction(self,face):
        try:
            face = cv2.resize(face, (self.shape_to_resize))
        except:
            pass
        face = self.preprocess_input(face, True)
        face = np.expand_dims(face, 0)
        face = np.expand_dims(face, -1)
        emotion_prediction = self.model.predict(face)
        emotion_label_arg = np.argmax(emotion_prediction)
        emotion_text = self.color_map[emotion_label_arg]
        return emotion_text