from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import pyautogui
import time

app = Flask(__name__)

# Function to count the number of fingers raised
def count_fingers(hand_landmarks):
    finger_count = 0
    threshold = (hand_landmarks.landmark[0].y * 100 - hand_landmarks.landmark[9].y * 100) / 2

    # Check if the index finger is raised
    if (hand_landmarks.landmark[5].y * 100 - hand_landmarks.landmark[8].y * 100) > threshold:
        finger_count += 1

    # Check if the middle finger is raised
    if (hand_landmarks.landmark[9].y * 100 - hand_landmarks.landmark[12].y * 100) > threshold:
        finger_count += 1

    # Check if the ring finger is raised
    if (hand_landmarks.landmark[13].y * 100 - hand_landmarks.landmark[16].y * 100) > threshold:
        finger_count += 1

    # Check if the pinky finger is raised
    if (hand_landmarks.landmark[17].y * 100 - hand_landmarks.landmark[20].y * 100) > threshold:
        finger_count += 1

    # Check if the thumb is raised
    if (hand_landmarks.landmark[5].x * 100 - hand_landmarks.landmark[4].x * 100) > 6:
        finger_count += 1

    return finger_count

# Initialize the MediaPipe hands model and webcam feed
video_capture = cv2.VideoCapture(0)
drawing_utils = mp.solutions.drawing_utils
hands_module = mp.solutions.hands
hand_detector = hands_module.Hands(max_num_hands=1)  # Detect one hand at a time

gesture_initialized = False
previous_finger_count = -1

def generate_frames():
    global gesture_initialized, previous_finger_count

    while True:
        current_time = time.time()
        success, frame = video_capture.read()

        if not success:
            break
        else:
            frame = cv2.flip(frame, 1)

            # Process the frame to detect hand landmarks
            results = hand_detector.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]

                finger_count = count_fingers(hand_landmarks)

                # Gesture control logic
                if not (previous_finger_count == finger_count):
                    if not gesture_initialized:
                        start_time = time.time()
                        gesture_initialized = True

                    elif (current_time - start_time) > 0.2:
                        if finger_count == 1:
                            pyautogui.press("right")

                        elif finger_count == 2:
                            pyautogui.press("left")

                        elif finger_count == 3:
                            pyautogui.press("up")

                        elif finger_count == 4:
                            pyautogui.press("down")

                        elif finger_count == 5:
                            pyautogui.press("space")

                        previous_finger_count = finger_count
                        gesture_initialized = False

                # Draw landmarks
                drawing_utils.draw_landmarks(frame, hand_landmarks, hands_module.HAND_CONNECTIONS)

            # Convert the frame to JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
