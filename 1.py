import cv2
import numpy as np
import pyautogui

cap = cv2.VideoCapture(0)

def analyze_hand(thresh, drawing):
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return "NONE", (0,0), 0

    cnt = max(contours, key=lambda x: cv2.contourArea(x))
    area = cv2.contourArea(cnt)

    hull = cv2.convexHull(cnt)
    cv2.drawContours(drawing, [cnt], -1, (0,255,0), 2)  # hand contour
    cv2.drawContours(drawing, [hull], -1, (0,255,255), 2)  # convex hull

    hull_indices = cv2.convexHull(cnt, returnPoints=False)
    defects = cv2.convexityDefects(cnt, hull_indices)
    
    # Count fingers
    fingers = 0
    if defects is not None:
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])
            a = np.linalg.norm(np.array(end)-np.array(start))
            b = np.linalg.norm(np.array(far)-np.array(start))
            c = np.linalg.norm(np.array(end)-np.array(far))
            angle = np.arccos((b**2 + c**2 - a**2)/(2*b*c+1e-6)) * 57
            if angle <= 90:
                fingers += 1
                cv2.circle(drawing, far, 6, (0,0,255), -1)  # defect points

    # Hand center
    M = cv2.moments(cnt)
    if M["m00"] != 0:
        cx = int(M["m10"]/M["m00"])
        cy = int(M["m01"]/M["m00"])
    else:
        cx, cy = 0, 0

    # Determine gesture based on fingers and area
    if area > 5000 and fingers >= 4:
        gesture = "PALM"       # palm open → aim
    elif fingers == 0 or area < 2000:
        gesture = "FIST"       # fist → shoot
    elif fingers == 1:
        gesture = "ONE"        # point → power
    else:
        gesture = "NONE"

    return gesture, (cx, cy), fingers

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    roi = frame[100:400, 100:400]
    cv2.rectangle(frame, (100,100), (400,400), (0,255,0),2)

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (35,35), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    drawing = np.zeros(roi.shape, np.uint8)
    gesture, center, fingers = analyze_hand(thresh, drawing)

    # Controls mapping
    if gesture == "PALM":
        if center[0] < 150:
            pyautogui.press("left")
            cv2.putText(frame,"AIM LEFT",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        else:
            pyautogui.press("right")
            cv2.putText(frame,"AIM RIGHT",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    elif gesture == "ONE":
        pyautogui.press("up")      # increase power
        cv2.putText(frame,"POWER UP",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
    elif gesture == "FIST":
        pyautogui.press("space")   # shoot
        cv2.putText(frame,"SHOOT!",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2)

    cv2.imshow("Frame", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Hand Lines", drawing)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
