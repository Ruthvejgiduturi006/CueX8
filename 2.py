import cv2
import mediapipe as mp
import pyautogui

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Screen center calibration
frame_center_x = 0
frame_center_y = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if frame_center_x == 0:
        frame_center_x = frame.shape[1] // 2
        frame_center_y = frame.shape[0] // 2

    gesture = "NONE"
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Index and thumb
            index_x = int(hand_landmarks.landmark[8].x * frame.shape[1])
            index_y = int(hand_landmarks.landmark[8].y * frame.shape[0])
            thumb_y = int(hand_landmarks.landmark[4].y * frame.shape[0])

            # Horizontal movement -> Aim
            if index_x < frame_center_x - 50:
                gesture = "LEFT"
                pyautogui.press("left")
            elif index_x > frame_center_x + 50:
                gesture = "RIGHT"
                pyautogui.press("right")

            # Vertical movement -> Power
            elif index_y > frame_center_y + 50:
                gesture = "POWER UP"
                pyautogui.press("down")
            elif index_y < frame_center_y - 50:
                gesture = "POWER DOWN"
                pyautogui.press("up")

            # Thumb check -> Shoot
            if thumb_y > index_y + 40:
                gesture = "SHOOT"
                pyautogui.press("space")

    cv2.putText(frame, f"Gesture: {gesture}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)
    cv2.imshow("Hand Control 8-Ball Pool", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
