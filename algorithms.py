import math
import threading
from playsound import playsound
def play_audio(file_path):
    threading.Thread(target=playsound, args=(file_path,)).start()
def caleyeposY(detection_result):
    left_eye=[1,2]
    right_eye=[4,5]
    left_eye_avgY=0
    right_eye_avgY=0
    cnt=0
    for num in left_eye:
        if detection_result.pose_landmarks[0][num].visibility > 0.6:
            left_eye_avgY+=detection_result.pose_landmarks[0][num].y
            cnt+=1
    if cnt==0:
        return False,False
    left_eye_avgY/=cnt
    cnt=0
    for num in right_eye:
        if detection_result.pose_landmarks[0][num].visibility > 0.6:
            right_eye_avgY+=detection_result.pose_landmarks[0][num].y
            cnt+=1
    if cnt==0:
        return False,False
    right_eye_avgY/=cnt
    return left_eye_avgY,right_eye_avgY
def calelbowposY(detection_result):
    left_elbow=detection_result.pose_landmarks[0][13].y
    right_elbow=detection_result.pose_landmarks[0][14].y
    return left_elbow,right_elbow
def calhandposY(detection_result):#average hight position Y of left hand and right hand
    left_hand = [16,18,20,22]
    right_hand = [15,17,19,21]
    left_avgY = 0
    right_avgY = 0
    cnt = 0
    for num in left_hand:
        if detection_result.pose_landmarks[0][num].visibility > 0.6:
            left_avgY += detection_result.pose_landmarks[0][num].y
            cnt+=1
    if cnt == 0:
        return False , False
    left_avgY /= cnt
    cnt = 0
    for num in right_hand:
        if detection_result.pose_landmarks[0][num].visibility > 0.6:
            right_avgY += detection_result.pose_landmarks[0][num].y
            cnt+=1
    if cnt == 0:
        return False , False
    right_avgY /= cnt
    return left_avgY , right_avgY

def calmouthposY(detection_result):#average hight position Y of mouth
    mouth = [9,10]
    avg = 0
    cnt = 0
    for num in mouth:
        if detection_result.pose_landmarks[0][num].visibility > 0.6:
            avg += detection_result.pose_landmarks[0][num].y
            cnt += 1
    if cnt == 0:
        return False , False
    return avg / cnt
def find_shoulder_posY(detection_result):
    left_shoulder=detection_result.pose_landmarks[0][11].y
    right_shoulder=detection_result.pose_landmarks[0][12].y
    return left_shoulder,right_shoulder

def angle(a,b,c):
    a = (a[0] , 1-a[1])
    b = (b[0] , 1-b[1])
    c = (c[0] , 1-c[1])
    ba = [a[0]-b[0] , a[1]-b[1]]
    bc = [c[0]-b[0] , c[1]-b[1]]
    ba_bc = ba[0]*bc[0] + ba[1]*bc[1]
    ba_len = (ba[0]**2 + ba[1]**2)**0.5
    bc_len = (bc[0]**2 + bc[1]**2)**0.5
    cos_angle = ba_bc / (ba_len * bc_len)
    angle = math.acos(cos_angle)*180/math.pi
    return angle
def if_hand_straight(detection_result):
    a = (detection_result.pose_landmarks[0][11].x , detection_result.pose_landmarks[0][11].y)
    b = (detection_result.pose_landmarks[0][13].x , detection_result.pose_landmarks[0][13].y)
    c = (detection_result.pose_landmarks[0][15].x , detection_result.pose_landmarks[0][15].y)
    d = (detection_result.pose_landmarks[0][12].x , detection_result.pose_landmarks[0][12].y)
    e = (detection_result.pose_landmarks[0][14].x , detection_result.pose_landmarks[0][14].y)
    f = (detection_result.pose_landmarks[0][16].x , detection_result.pose_landmarks[0][16].y)
    g = (detection_result.pose_landmarks[0][23].x , detection_result.pose_landmarks[0][23].y)
    h = (detection_result.pose_landmarks[0][24].x , detection_result.pose_landmarks[0][24].y)
    left_angle = angle(a,b,c)
    right_angle = angle(d,e,f)
    #print(left_angle,right_angle)
    cirteria = 100
    if left_angle < cirteria or right_angle < cirteria:
        return False
    else:
        return True
def if_body_straight(detection_result):
    
    
    left_shoulder = detection_result.pose_landmarks[0][11].y
    right_shoulder = detection_result.pose_landmarks[0][12].y
    left_hip = detection_result.pose_landmarks[0][23].y
    right_hip = detection_result.pose_landmarks[0][24].y
    
    shoulder_difference=abs(left_shoulder-right_shoulder)
    hip_difference=abs(left_hip-right_hip)
    standard=0.1  #can change it freely
    if shoulder_difference<standard and hip_difference<standard:
        return True
    else:
        return False
def if_shoulder_up(previous_left,current_left,previous_right,current_right):
    if (current_left<previous_left-0.005) and (current_right<previous_right-0.005):
        return True
    else:
        return False
def if_shoulder_down(previous_left,current_left,previous_right,current_right):
    if (current_left>previous_left+0.005) and (current_right>previous_right+0.005):
        return True
    else:
        return False
def if_shoulder_stable(previous_left,current_left,previous_right,current_right):
    if (previous_left-0.01<=current_left<=previous_left+0.01) and (previous_right-0.01<=current_right<=previous_right+0.01):
        return True
    else:
        return False
def if_hands_symmetric(detection_result):
    lefthand,righthand=calhandposY(detection_result)
    standard=0.2 #can change it freely
    if abs(righthand-lefthand)<standard:
        return True
    else:
        return False
    
def if_shoulder_symmetric(detection_result):
    left_shoulder = detection_result.pose_landmarks[0][11].y
    right_shoulder = detection_result.pose_landmarks[0][12].y
    left_hand, right_hand = calhandposY(detection_result)
    standard=abs(left_hand-right_hand)+0.001
    if abs(left_shoulder-right_shoulder)<standard:
        return True
    else:
        return False
