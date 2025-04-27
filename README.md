# Pull-Up Real-Time Gesture Feedback System

This project is a real-time gesture feedback system designed to assist users in performing pull-ups with proper form. The system uses computer vision to analyze body posture and provides audio feedback to encourage correct movements and discourage improper form.

## Features

- **Real-Time Feedback**: Detects body posture and provides immediate feedback during pull-ups.
- **Audio Guidance**: Plays audio cues to encourage proper form and motivate the user.
- **Form Validation**:
  - Checks if the body is straight.
  - Ensures hands are symmetric.
  - Validates hand and shoulder movements.
- **Progress Tracking**: Counts the number of successful pull-ups and provides milestone encouragement (e.g., every 5 or 10 pull-ups).
- **Error Detection**: Identifies common mistakes such as:
  - Body not straight.
  - Hands not symmetric.
  - Incomplete pull-ups.

## System Requirements

- Python 3.7 or higher
- Required Python libraries:
  - `mediapipe`
  - `opencv-python`
  - `imutils`
  - `playsound`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/pull-up-feedback-system.git
   cd pull-up-feedback-system
   ```
2. Use existing video for input:
- Put the video in testpictures/
- Comment ln 85 of main.py and enable ln 86
- Change the video name in openexistingvideo.py, rotate the video by enabling ln 17
