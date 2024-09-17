#This file is just raw code of implementation and doesn't contribute to final project, therefore all code is commented

# Import necessary libraries
import cv2  # OpenCV for video capture and image processing
import mediapipe as mp  # MediaPipe for hand detection and gesture recognition
import pyautogui  # pyautogui for simulating keyboard presses
import time  # Time library for gesture timing

# Function to count the number of fingers raised based on hand landmarks
def count_fingers(hand_landmarks):
    finger_count = 0  # Initialize a variable to store the count of raised fingers

    # Threshold to differentiate between raised and lowered fingers based on hand landmarks
    threshold = (hand_landmarks.landmark[0].y * 100 - hand_landmarks.landmark[9].y * 100) / 2

    # Check if the index finger is raised by comparing the y-coordinate of landmarks 5 and 8
    if (hand_landmarks.landmark[5].y * 100 - hand_landmarks.landmark[8].y * 100) > threshold:
        finger_count += 1  # Increment finger count if the index finger is raised

    # Check if the middle finger is raised by comparing the y-coordinate of landmarks 9 and 12
    if (hand_landmarks.landmark[9].y * 100 - hand_landmarks.landmark[12].y * 100) > threshold:
        finger_count += 1  # Increment finger count if the middle finger is raised

    # Check if the ring finger is raised by comparing the y-coordinate of landmarks 13 and 16
    if (hand_landmarks.landmark[13].y * 100 - hand_landmarks.landmark[16].y * 100) > threshold:
        finger_count += 1  # Increment finger count if the ring finger is raised

    # Check if the pinky finger is raised by comparing the y-coordinate of landmarks 17 and 20
    if (hand_landmarks.landmark[17].y * 100 - hand_landmarks.landmark[20].y * 100) > threshold:
        finger_count += 1  # Increment finger count if the pinky finger is raised

    # Check if the thumb is raised by comparing the x-coordinate of landmarks 5 and 4
    if (hand_landmarks.landmark[5].x * 100 - hand_landmarks.landmark[4].x * 100) > 6:
        finger_count += 1  # Increment finger count if the thumb is raised

    return finger_count  # Return the total count of raised fingers

# Start capturing video from the webcam
video_capture = cv2.VideoCapture(0)  # Initialize video capture object to read from the default webcam

# Initialize the MediaPipe drawing utilities and hand detection modules
drawing_utils = mp.solutions.drawing_utils  # For drawing hand landmarks on the video frame
hands_module = mp.solutions.hands  # For hand detection and tracking using MediaPipe's Hands module
hand_detector = hands_module.Hands(max_num_hands=1)  # Detect a maximum of one hand at a time

# Initialize variables to track gesture initialization and previous finger count
gesture_initialized = False  # Tracks whether a gesture has started or not
previous_finger_count = -1  # Stores the previous number of fingers raised

# Main loop to process each frame from the webcam
while True:
    current_time = time.time()  # Get the current time for gesture timing
    _, frame = video_capture.read()  # Read a frame from the webcam
    frame = cv2.flip(frame, 1)  # Flip the frame horizontally for a mirror-like effect

    # Process the frame using the hand detector to identify hand landmarks
    results = hand_detector.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Check if hand landmarks are detected
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]  # Get the key points (landmarks) of the detected hand

        # Count the number of fingers raised based on the hand landmarks
        finger_count = count_fingers(hand_landmarks)

        # Check if the current finger count is different from the previous one (i.e., a new gesture)
        if not (previous_finger_count == finger_count):
            # If the gesture is new and not yet initialized, start timing it
            if not (gesture_initialized):
                start_time = time.time()  # Record the start time of the gesture
                gesture_initialized = True  # Mark the gesture as initialized

            # If the gesture is held for more than 0.2 seconds, it's considered valid
            elif (current_time - start_time) > 0.2:
                # Map the number of raised fingers to specific keyboard actions
                if (finger_count == 1):
                    pyautogui.press("right")  # Simulate pressing the right arrow key if 1 finger is raised

                elif (finger_count == 2):
                    pyautogui.press("left")  # Simulate pressing the left arrow key if 2 fingers are raised

                elif (finger_count == 3):
                    pyautogui.press("up")  # Simulate pressing the up arrow key if 3 fingers are raised

                elif (finger_count == 4):
                    pyautogui.press("down")  # Simulate pressing the down arrow key if 4 fingers are raised

                elif (finger_count == 5):
                    pyautogui.press("space")  # Simulate pressing the space bar if 5 fingers are raised

                # Update the previous finger count and reset the gesture initialization flag
                previous_finger_count = finger_count
                gesture_initialized = False

        # Draw the detected hand landmarks on the frame for visualization
        drawing_utils.draw_landmarks(frame, hand_landmarks, hands_module.HAND_CONNECTIONS)

    # Display the frame with hand landmarks in a window titled "Media Control"
    cv2.imshow("Media Control", frame)

    # Exit the loop if the 'Esc' key (key code 27) is pressed
    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()  # Close all OpenCV windows
        video_capture.release()  # Release the webcam
        break  # Exit the loop
