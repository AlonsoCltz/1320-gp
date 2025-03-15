# STEP 1: Import the necessary modules.
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import imutils
from imutils.video import VideoStream
#import pandas as pd
#import joblib
import pathlib
import premodel
import glob


def draw_landmarks_on_image(image, detection_result):
    # Make a writable copy of the image
    image = image.copy()
    for pose_landmarks in detection_result.pose_landmarks:
        for i in range(0, 33):
            landmark = pose_landmarks[i]
            x = int(landmark.x * image.shape[1])
            y = int(landmark.y * image.shape[0])
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
            cv2.putText(image, f'{i}', (x-5, y+3 ), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (225,0, 0), 1)
            
    return image


data_files = glob.glob('testpictures/*.jpg')

for file_path in data_files:
    image = cv2.imread(file_path)
    if image is not None:
        processed_image = premodel.imageprocess(image)
        detection_result = premodel.input_image(processed_image)

        annotated_image = draw_landmarks_on_image(processed_image.numpy_view(), detection_result)
        # flipped_annotated_image = cv2.flip(annotated_image, 1)
        
        # cv2.imshow('Annotated Image', cv2.cvtColor(flipped_annotated_image, cv2.COLOR_RGB2BGR))
        cv2.imshow('Annotated Image', cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
        cv2.waitKey(0)

cv2.destroyAllWindows()
