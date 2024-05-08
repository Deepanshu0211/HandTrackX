# HandTrackX

HandTrackX is a real-time hand tracking and gesture control system using computer vision techniques and the MediaPipe library. With HandTrackX, you can control your mouse cursor, perform left and right clicks, and even switch between screens with simple hand movements.

## Features

- Hand Tracking: The system accurately detects and tracks hand movements in real-time.
- Mouse Cursor Control: Move your hand to control the mouse cursor on the screen.
- Left Click: Tap your thumb and index finger to perform a left-click.
- Right Click: Tap your thumb and middle finger to perform a right-click.
- Screen Switching: Bring your thumb and middle finger close together to switch between screens.

## Requirements

- Python 3.x
- OpenCV
- Mediapipe
- Numpy
- PyAutoGUI

## Installation

1. Clone the repository:

  `git clone https://github.com/Deepanshu0211/handtrackx.git`


2. Install the required Python packages:

  `pip install opencv-python mediapipe numpy pyautogui`


## Usage

1. Run the `handtrackx.py` script:

  `python handtrackx.py`


2. Adjust your hand in front of the camera until it's detected.

3. Perform gestures as described in the Features section.

## Customization

- You can adjust the sensitivity of the gestures and mouse control by modifying the constants in the script.
- Change `TAP_DISTANCE_THRESHOLD` to adjust the distance required for a tap gesture.
- Modify `SMOOTHING` to change the smoothness of the mouse cursor movement.
- Adjust `CURSOR_OFFSET_X` and `CURSOR_OFFSET_Y` to fine-tune the cursor position.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
