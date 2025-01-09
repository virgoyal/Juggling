import cv2
import numpy as np


BALL_COLOR_LOWER = (17, 165, 50)
BALL_COLOR_UPPER = (22, 205, 140)


trajectory = []


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access the camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read the frame.")
        break

    frame = cv2.flip(frame, 1)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)


    mask = cv2.inRange(hsv, BALL_COLOR_LOWER, BALL_COLOR_UPPER)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)


    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)

        if radius > 10 and cv2.contourArea(c) > 500:
  
            if trajectory:
                x = int(0.7 * trajectory[-1][0] + 0.3 * x)
                y = int(0.7 * trajectory[-1][1] + 0.3 * y)


            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.putText(frame, f"Ball: {int(x)}, {int(y)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)


            trajectory.append((int(x), int(y)))
            if len(trajectory) > 50:
                trajectory.pop(0)


    for i in range(1, len(trajectory)):
        color = (i * 5 % 255, 255 - i * 5 % 255, 150)
        cv2.line(frame, trajectory[i - 1], trajectory[i], color, 2)


    cv2.imshow("Ball Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
