import cv2
import mediapipe as mp
import pyautogui

# Mediapipe setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)

def count_fingers(hand_landmarks):
    finger_tips = [8, 12, 16, 20]
    finger_fold = [6, 10, 14, 18]

    fingers = []

    # Thumb
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # 4 Fingers
    for tip, fold in zip(finger_tips, finger_fold):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[fold].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Count fingers
            finger_count = count_fingers(hand_landmarks)

            # Map gestures to controls
            if finger_count == 1:
                pyautogui.moveRel(20, 0)  # Aim
                cv2.putText(frame, "AIMING", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            elif finger_count == 2:
                pyautogui.dragRel(0, 20, duration=0.2)  # Select Power
                cv2.putText(frame, "SELECT POWER", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

            elif finger_count == 5:
                pyautogui.click()  # Shoot
                cv2.putText(frame, "SHOOT!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

            elif finger_count == 0:
                cv2.putText(frame, "STOP / RESET", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

    cv2.imshow("8 Ball Pool Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
