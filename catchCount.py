import cv2
import numpy as np

# Constants
LINE1_Y = 200  # Y-coordinate for the first line
LINE2_Y = 400  # Y-coordinate for the second line
BALL_COLOR_LOWER = (18,105 ,146)  # Example HSV color range for the ball (adjust as needed)
BALL_COLOR_UPPER = (25, 140, 232)
THROW_COUNT = 0
CATCH_COUNT = 0

# Initialize tracking variables
ball_last_y = None
ball_direction = None

# Open the camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access the camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read the frame.")
        break

    # Flip frame (optional, depending on camera orientation)
    frame = cv2.flip(frame, 1)

    # Convert to HSV for color detection
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Mask for the ball color
    mask = cv2.inRange(hsv, BALL_COLOR_LOWER, BALL_COLOR_UPPER)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    # Find contours of the masked ball
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # Get the largest contour (assuming it's the ball)
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)

        if radius > 10:  # Minimum size to filter out noise
            # Draw the ball on the frame
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.putText(frame, f"Ball: {int(x)}, {int(y)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # Detect crossing events
            if ball_last_y is not None:
                if ball_last_y < LINE1_Y <= y:  # Ball crossing down Line 1
                    ball_direction = "down"
                elif ball_last_y > LINE2_Y >= y:  # Ball crossing up Line 2
                    ball_direction = "up"

                if ball_direction == "down" and y >= LINE2_Y:
                    THROW_COUNT += 1
                    ball_direction = None
                elif ball_direction == "up" and y <= LINE1_Y:
                    CATCH_COUNT += 1
                    ball_direction = None

            ball_last_y = y

    # Draw the lines
    cv2.line(frame, (0, LINE1_Y), (frame.shape[1], LINE1_Y), (255, 0, 0), 2)
    cv2.line(frame, (0, LINE2_Y), (frame.shape[1], LINE2_Y), (0, 0, 255), 2)

    # Display counters
    cv2.putText(frame, f"Throws: {THROW_COUNT}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, f"Catches: {CATCH_COUNT}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Show the frame
    cv2.imshow("Juggling Tracker", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
