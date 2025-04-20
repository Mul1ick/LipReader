import cv2
import dlib
import numpy as np
from skimage.transform import resize
from imutils import face_utils, resize as imutils_resize
from tensorflow.keras.models import load_model

# Load your pretrained model
model = load_model('//Users//aryanmullick//Downloads//lipreading_model.keras')

# Word labels (in order of the softmax output)
word_labels = ['Begin', 'Choose', 'Connection', 'Navigation', 'Next', 'Previous', 'Start', 'Stop', 'Hello', 'Web']

# Shape predictor path (you'll need to upload this file as well)
predictor_path = '//Users//aryanmullick//Downloads//shape_predictor_68_face_landmarks.dat'
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

def preprocess_video(video_path):
    cap = cv2.VideoCapture(video_path)
    sequence = []

    while len(sequence) < 22:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (500, int(frame.shape[0] * 500 / frame.shape[1])))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 1)

        if len(rects) == 1:
            shape = predictor(gray, rects[0])
            shape = face_utils.shape_to_np(shape)
            (x, y, w, h) = cv2.boundingRect(np.array([shape[48:68]]))
            roi = gray[y:y+h, x:x+w]

            # Force size to 100x100
            try:
                roi = cv2.resize(roi, (100, 100))
                sequence.append(roi)
            except Exception as e:
                print(f"Error resizing frame: {e}")
    
    cap.release()

    while len(sequence) < 22:
        sequence.append(np.zeros((100, 100), dtype=np.uint8))

    # Debug: Print all shapes before converting to array
    for i, frame in enumerate(sequence):
        print(f"Frame {i} shape: {frame.shape}")

    sequence = np.array(sequence)  # should now work
    sequence = sequence.astype(np.float32)
    v_min, v_max = sequence.min(), sequence.max()
    sequence = (sequence - v_min) / (v_max - v_min + 1e-6)

    sequence = np.expand_dims(sequence, axis=-1)
    sequence = np.expand_dims(sequence, axis=0)

    return sequence

def predict_word(preprocessed_input):
    preds = model.predict(preprocessed_input)
    return word_labels[np.argmax(preds)]