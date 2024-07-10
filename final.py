import cv2 
import mediapipe as mp
import pyautogui
import time

# Function to count the number of fingers raised
def count_fingers(hand_landmarks):
    finger_count = 0

    # Threshold to distinguish between raised and lowered fingers
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

# Start capturing video from the webcam
video_capture = cv2.VideoCapture(0)

drawing_utils = mp.solutions.drawing_utils
hands_module = mp.solutions.hands
hand_detector = hands_module.Hands(max_num_hands=1)  # Detect one hand at a time

gesture_initialized = False  # Variable to track the start of a gesture
previous_finger_count = -1  # Variable to store the previous gesture count

while True:
    current_time = time.time()
    _, frame = video_capture.read()  # Read a frame from the webcam
    frame = cv2.flip(frame, 1)  # Flip the frame horizontally

    # Process the frame to detect hand landmarks
    results = hand_detector.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]  # Get the key points of the detected hand

        finger_count = count_fingers(hand_landmarks)  # Count the number of raised fingers

        # Check if the current gesture is different from the previous one
        if not (previous_finger_count == finger_count):
            if not (gesture_initialized):
                start_time = time.time()  # Start timing the gesture
                gesture_initialized = True

            elif (current_time - start_time) > 0.2:  # Check if the gesture is held for 0.2 seconds
                if (finger_count == 1):
                    pyautogui.press("right")  # Press the right arrow key

                elif (finger_count == 2):
                    pyautogui.press("left")  # Press the left arrow key

                elif (finger_count == 3):
                    pyautogui.press("up")  # Press the up arrow key

                elif (finger_count == 4):
                    pyautogui.press("down")  # Press the down arrow key

                elif (finger_count == 5):
                    pyautogui.press("space")  # Press the space bar

                previous_finger_count = finger_count  # Update the previous gesture count
                gesture_initialized = False  # Reset the gesture initialization

        # Draw the hand landmarks on the frame
        drawing_utils.draw_landmarks(frame, hand_landmarks, hands_module.HAND_CONNECTIONS)

    cv2.imshow("Media Control", frame)  # Display the frame

    if cv2.waitKey(1) == 27:  # Exit the loop if the 'Esc' key is pressed
        cv2.destroyAllWindows()
        video_capture.release()
        break