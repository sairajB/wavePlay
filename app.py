from flask import Flask, render_template, Response, request
import cv2
import mediapipe as mp
import pyautogui
import time
import threading

app = Flask(__name__)

streaming = False
video_capture = None
hand_detector = None

def initialize_components():
    global video_capture, hand_detector
    # Initialize the webcam
    video_capture = cv2.VideoCapture(0)
    # Initialize MediaPipe hands model
    hand_detector = mp.solutions.hands.Hands(max_num_hands=1)

# Initialize components in a separate thread
threading.Thread(target=initialize_components).start()

def count_fingers(hand_landmarks):
    finger_count = 0
    threshold = (hand_landmarks.landmark[0].y * 100 - hand_landmarks.landmark[9].y * 100) / 2

    if (hand_landmarks.landmark[5].y * 100 - hand_landmarks.landmark[8].y * 100) > threshold:
        finger_count += 1

    if (hand_landmarks.landmark[9].y * 100 - hand_landmarks.landmark[12].y * 100) > threshold:
        finger_count += 1

    if (hand_landmarks.landmark[13].y * 100 - hand_landmarks.landmark[16].y * 100) > threshold:
        finger_count += 1

    if (hand_landmarks.landmark[17].y * 100 - hand_landmarks.landmark[20].y * 100) > threshold:
        finger_count += 1

    if (hand_landmarks.landmark[5].x * 100 - hand_landmarks.landmark[4].x * 100) > 6:
        finger_count += 1

    return finger_count

drawing_utils = mp.solutions.drawing_utils
hands_module = mp.solutions.hands

gesture_initialized = False
previous_finger_count = -1

def generate_frames():
    global gesture_initialized, previous_finger_count, video_capture, streaming, hand_detector

    while streaming:
        if video_capture is None or hand_detector is None:
            time.sleep(0.1)  # Wait for initialization
            continue

        current_time = time.time()
        success, frame = video_capture.read()

        if not success or not streaming:
            break
        else:
            frame = cv2.flip(frame, 1)

            results = hand_detector.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                finger_count = count_fingers(hand_landmarks)

                if previous_finger_count != finger_count:
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

                drawing_utils.draw_landmarks(frame, hand_landmarks, hands_module.HAND_CONNECTIONS)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_video', methods=['POST'])
def start_video():
    global streaming
    streaming = True
    return '', 204

@app.route('/video_feed')
def video_feed():
    global streaming
    if streaming:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return '', 204

@app.route('/stop_video', methods=['POST'])
def stop_video():
    global streaming
    streaming = False
    return '', 204

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8000)))
