import cv2
import mediapipe as mp
import numpy as np
import pyautogui

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

MOUSE_CONTROL_WIDTH = SCREEN_WIDTH // 2
MOUSE_CONTROL_HEIGHT = SCREEN_HEIGHT // 2

ZOOM_FACTOR = 1.2

SMOOTHING = 0.5

CURSOR_OFFSET_X = 20
CURSOR_OFFSET_Y = 20

TAP_DISTANCE_THRESHOLD = 30

FRAME_WIDTH = SCREEN_WIDTH
FRAME_HEIGHT = SCREEN_HEIGHT

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

cap.set(3, FRAME_WIDTH)
cap.set(4, FRAME_HEIGHT)

thumb_index_distance = None
zoom_flag = False
tap_flag = False
tap_frame_count = 0

smoothed_mouse_x, smoothed_mouse_y = 0, 0

screen_number = 1
total_screens = pyautogui.screenshot().size[0] // SCREEN_WIDTH

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            thumb_lm = hand_landmarks.landmark[4]
            index_finger_lm = hand_landmarks.landmark[8]
            middle_finger_lm = hand_landmarks.landmark[12]

            tx, ty = int(thumb_lm.x * frame.shape[1]), int(thumb_lm.y * frame.shape[0])
            ix, iy = int(index_finger_lm.x * frame.shape[1]), int(index_finger_lm.y * frame.shape[0])
            mx, my = int(middle_finger_lm.x * frame.shape[1]), int(middle_finger_lm.y * frame.shape[0])

            thumb_index_distance_new = np.sqrt((tx - ix) ** 2 + (ty - iy) ** 2)

            if thumb_index_distance is not None:
                if thumb_index_distance_new < thumb_index_distance:
                    zoom_flag = True
                else:
                    zoom_flag = False
            thumb_index_distance = thumb_index_distance_new

            mouse_x = np.interp(ix, (0, frame.shape[1]), (0, MOUSE_CONTROL_WIDTH))
            mouse_y = np.interp(iy, (0, frame.shape[0]), (0, MOUSE_CONTROL_HEIGHT))

            smoothed_mouse_x = smoothed_mouse_x + SMOOTHING * (mouse_x - smoothed_mouse_x)
            smoothed_mouse_y = smoothed_mouse_y + SMOOTHING * (mouse_y - smoothed_mouse_y)

            cursor_x = int(smoothed_mouse_x) + CURSOR_OFFSET_X
            cursor_y = int(smoothed_mouse_y) + CURSOR_OFFSET_Y

            pyautogui.moveTo(cursor_x, cursor_y, duration=0.1)

            if thumb_index_distance_new < TAP_DISTANCE_THRESHOLD:
                if tap_frame_count == 0:
                    tap_flag = True
                tap_frame_count += 1
            else:
                if 0 < tap_frame_count < 10:
                    pyautogui.click(button='left')
                tap_frame_count = 0
                tap_flag = False

            if thumb_index_distance_new < TAP_DISTANCE_THRESHOLD and my < iy:
                pyautogui.click(button='right')

            # Swap screen if thumb and middle finger are close
            if thumb_index_distance_new < TAP_DISTANCE_THRESHOLD:
                if mx < ix:
                    screen_number -= 1
                    if screen_number < 1:
                        screen_number = total_screens
                    pyautogui.hotkey('win', str(screen_number))
                elif mx > ix:
                    screen_number += 1
                    if screen_number > total_screens:
                        screen_number = 1
                    pyautogui.hotkey('win', str(screen_number))

    cv2.imshow('Hand Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
