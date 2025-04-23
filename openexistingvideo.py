import cv2

# Open the video file
video_path = 'testpictures/firsttest.mp4'
cap = cv2.VideoCapture(video_path)
# Get the total number of frames
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
# Calculate the middle frame index
#middle_frame = total_frames // 2
# Set the video capture position to the middle frame
#cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame)
def readvideo(cap):
    ret, frame = cap.read()
    if not ret:
        return None
    # Rotate the frame 90 degrees clockwise
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    return frame





