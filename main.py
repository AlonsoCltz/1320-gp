import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import imutils
from imutils.video import VideoStream
import premodel
import openexistingvideo
import algorithms
from algorithms import *

def draw_landmarks_on_image(image, detection_result):
    # Make a writable copy of the image
    image = image.copy()
    #print(len(detection_result.pose_landmarks))
    if len(detection_result.pose_landmarks) == 0:
        return image
    pose_landmarks = detection_result.pose_landmarks[0]
    for i in range(0,33):
    #for landmark in pose_landmarks:  # Corrected line
        landmark = pose_landmarks[i]
        x = int(landmark.x * image.shape[1])
        y = int(landmark.y * image.shape[0])
        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
        #print(landmark)
        #[[]]
        #cv2.putText(image, f'{i} {x} {y}', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.putText(image, f'{i}', (x-5, y+3 ), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (225,0, 0), 1)
    return image


'''
vs = VideoStream(src=0).start()  # 開啟攝影機

# Add error handling for camera
if not vs.stream.isOpened():
    print("Error: Could not open video stream.")
    exit()
'''

now_status = 0 #set the current status to stand by mode
count=0
status = {0:'stand by', 1: 'raise hand', 2: 'rising', 3: 'at the top waiting to come down', 4: 'falling', 5: 'at bottom'}
cap = openexistingvideo.cap
cntfps = 0 #每5次检查手部位置,比较肩膀是否上升
cntfpsthreshold = 4
cntfpsthreshold2 = 1
previous_shoulder_left,previous_shoulder_right=0,0
previous_hand_left,previous_hand_right=0,0

atBottomadded = False#prevent from multiple count at bottom
can_count = False #make sure he already get on the top
while True:

    '''frame = vs.read()'''
    frame = openexistingvideo.readvideo(cap)
    #print(frame)
    if frame is not None:
        #print('running')
        frame = cv2.flip(frame,1)
        image = premodel.imageprocess(frame)

        detection_result = premodel.input_image(image)
        
        
        annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result)



        cv2.putText(annotated_image, f'{status[now_status]}', (5,50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 1)
        
        
        if len(detection_result.pose_landmarks) == 0:
            cv2.imshow('Annotated Image', cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
            if cv2.waitKey(10) == 27:
                break
            continue
        #the format for detection result will be x, y, z, visibility, presence
        #use detection_result.pose_landmarks[n].x to retrieve data
        left_eye_avgY,right_eye_avgY=caleyeposY(detection_result)
        left_hand_avgY , right_hand_avgY = calhandposY(detection_result)
        mouth_avgY = calmouthposY(detection_result)
        #jaw_avg=caljawposY(detection_result)
        if now_status != 5:
            atBottomadded = False
        if now_status == 0: #standing by
            
            if left_hand_avgY != False and mouth_avgY != False:

                if left_hand_avgY < mouth_avgY and right_hand_avgY < mouth_avgY:
                    now_status = 1
        elif now_status == 1:#raise hand:
            cntfps += 1
            if left_hand_avgY != False and mouth_avgY != False:
                if not(left_hand_avgY < mouth_avgY and right_hand_avgY < mouth_avgY):
                    now_status = 0
            if cntfps == cntfpsthreshold:
                cntfps = 0
                current_shoulder_left,current_shoulder_right=find_shoulder_posY(detection_result)
                if if_shoulder_up(previous_shoulder_left,current_shoulder_left,previous_shoulder_right,current_shoulder_right):
                    previous_shoulder_left,previous_shoulder_right=current_shoulder_left,current_shoulder_right
                    now_status = 2
                else:
                    previous_shoulder_left,previous_shoulder_right=current_shoulder_left,current_shoulder_right
                    now_status = 4
        elif now_status == 2:#rising
            cntfps += 1
            if cntfps == cntfpsthreshold:
                cntfps = 0
                current_shoulder_left,current_shoulder_right=find_shoulder_posY(detection_result)
                if if_shoulder_down(previous_shoulder_left,current_shoulder_left,previous_shoulder_right,current_shoulder_right):
                    now_status = 4
                
                if if_shoulder_up(previous_shoulder_left,current_shoulder_left,previous_shoulder_right,current_shoulder_right) and left_hand_avgY != False and mouth_avgY != False:
                    if not(left_hand_avgY < mouth_avgY and right_hand_avgY < mouth_avgY):
                        
                        #previous_shoulder_left,previous_shoulder_right=find_shoulder_posY(detection_result)
                        
                        if (if_body_straight(detection_result)) and (if_hands_symmetric(detection_result)):  #这一行是可以的

                            current_shoulder_left,current_shoulder_right=find_shoulder_posY(detection_result)
                            now_status=3
                            '''
                            if (left_hand_avgY>left_eye_avgY) and (if_shoulder_up(previous_shoulder_left,current_shoulder_left,previous_shoulder_right,current_shoulder_right)):  #这一行我看不懂，再想想吧
                                
                                
                            else:
                                now_status=0'''
                        else:
                            print('here')
                            now_status = 0
                previous_shoulder_left,previous_shoulder_right=current_shoulder_left,current_shoulder_right
        elif now_status == 3: #at the top waiting to come down
            if left_hand_avgY != False and mouth_avgY != False:
                if left_hand_avgY < mouth_avgY and right_hand_avgY < mouth_avgY:# and jaw_avg>left_hand_avgY:
                    now_status = 4
                    can_count = True
        elif now_status == 4: #falling
            cntfps += 1
            if cntfps == cntfpsthreshold:
                cntfps = 0
                current_shoulder_left,current_shoulder_right=find_shoulder_posY(detection_result)
                if if_shoulder_up(previous_shoulder_left,current_shoulder_left,previous_shoulder_right,current_shoulder_right):
                    now_status = 2
                    print('not too fast')
                elif if_shoulder_stable(previous_shoulder_left,current_shoulder_left,previous_shoulder_right,current_shoulder_right):
                    now_status = 5
                previous_shoulder_left,previous_shoulder_right=current_shoulder_left,current_shoulder_right
        elif now_status == 5: #at bottom
            cntfps += 1
            if cntfps == cntfpsthreshold:
                cntfps = 0
                current_shoulder_left,current_shoulder_right=find_shoulder_posY(detection_result)
                if if_shoulder_up(previous_shoulder_left,current_shoulder_left,previous_shoulder_right,current_shoulder_right):
                    now_status = 2
                elif if_shoulder_down(previous_shoulder_left,current_shoulder_left,previous_shoulder_right,current_shoulder_right):
                    now_status = 4
                if (if_body_straight(detection_result)) and (if_hands_symmetric(detection_result)) and (if_hand_straight(detection_result)):
                    if (not atBottomadded) and can_count:
                        count+=1
                        can_count = False
                    atBottomadded = True
                elif not (if_body_straight(detection_result)):
                    print('body not straight')
                elif not (if_hands_symmetric(detection_result)):
                    print('not symmetric')
                elif not (if_hand_straight(detection_result)):
                    print('hand not straight')
                previous_shoulder_left,previous_shoulder_right=current_shoulder_left,current_shoulder_right
                
        try:
            cv2.putText(annotated_image, f'pre: {round(previous_shoulder_left,3)} now: {round(current_shoulder_left,3)}', (5,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
            cv2.putText(annotated_image, f'Count: {count}', (5,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
        except:
            pass
        

        
                



            
        
        
        cv2.imshow('Annotated Image', cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
        if cv2.waitKey(10) == 27:
            break

cv2.destroyAllWindows()
cap.release()
'''vs.stop()'''
