# WavePlay

## Description

WavePlay is a project designed to facilitate hands-free interaction with computers, particularly for individuals with disabilities. By leveraging real-time hand gesture recognition, this project enables users to control keyboard actions without the need for traditional input devices such as keyboards or mice.

## Table of Contents

- [How It Works](#how-it-works)
- [Features](#features)
- [Use Case](#use-case)
- [Usage](#usage)
- [License](#license)

## How It Works

The system utilizes the following technologies:

- **MediaPipe**: For detecting and tracking hand landmarks in real-time using a webcam.
- **OpenCV**: For processing video frames and visualizing hand landmarks.
- **PyAutoGUI**: For simulating keyboard inputs based on detected hand gestures.

The application captures video from a webcam, processes each frame to detect the position of hand landmarks, and interprets specific gestures to trigger corresponding keyboard actions. This allows users to perform functions such as navigating through applications or executing commands with simple hand movements.

## Features

- **Gesture Recognition**: Identifies and interprets hand gestures to perform keyboard actions.
- **Real-Time Feedback**: Displays hand landmarks on the video feed for easy tracking.
- **Customizable**: Supports different gestures for various keyboard actions.

## Use Case

This tool is particularly beneficial for individuals who may have difficulty using traditional input devices due to physical limitations. By recognizing and mapping hand gestures to keyboard commands, users can interact with their computers in a more accessible and intuitive way.

## Usage

To start using the WavePlay application:

1. Ensure your webcam is connected and working.
2. Run the application:
    ```sh
    python main.py
    ```
3. Perform gestures in front of the webcam to simulate keyboard actions:
    - **1 Finger Raised**: Simulates pressing the right arrow key.
    - **2 Fingers Raised**: Simulates pressing the left arrow key.
    - **3 Fingers Raised**: Simulates pressing the up arrow key.
    - **4 Fingers Raised**: Simulates pressing the down arrow key.
    - **5 Fingers Raised**: Simulates pressing the space key.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
