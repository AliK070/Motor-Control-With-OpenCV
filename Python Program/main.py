import cv2
import mediapipe as mp
import time
import math
import pyfirmata2

# Initialize Arduino
board = pyfirmata2.Arduino("COM5")
motorSpeedpin = board.get_pin("d:6:p")  # Use digital pin D5 for PWM (p stands for PWM output)
motorSpeedpin2 = board.get_pin("d:5:p")  # Use digital pin D5 for PWM (p stands for PWM output)
ain1 = board.get_pin("d:13:o")          # Motor direction control pin
ain2 = board.get_pin("d:12:o")          # Motor direction control pin

bin1 = board.get_pin("d:8:o")          # Motor direction control pin
bin2 = board.get_pin("d:4:o")          # Motor direction control pin

# Global variable to store the distance value
dist_val = 0  

# Mediapipe initialization
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# OpenCV settings
capture = cv2.VideoCapture(0)

# Colors and fonts
c_green = (0, 200, 0)
c_black = (90, 40, 20)
f_small = cv2.FONT_HERSHEY_PLAIN
f_size = 2
prevTime = 0

# Draw FPS on the frame
def drawFPS(frame):
    global prevTime
    currentTime = time.time()
    fps = 1 / (currentTime - prevTime)
    prevTime = currentTime
    cv2.putText(frame, f"FPS: {int(fps)}", (40, 70), f_small, f_size, c_green, 2)

# Draw line between thumb and pinky, calculate distance
def drawLineTP(frame, hand_landmarks):
    global dist_val
    thumb_tip = hand_landmarks.landmark[4]
    pinky_tip = hand_landmarks.landmark[20]

    # Calculate distance
    distance = round(
        100
        * math.sqrt(
            ((thumb_tip.x - pinky_tip.x) ** 2 + (thumb_tip.y - pinky_tip.y) ** 2)
        )
    )
    dist_val = distance  # Update the global distance variable

    # Display the distance on the frame
    cv2.putText(frame, f"Distance: {int(distance)}", (350, 70), f_small, f_size, c_green, 2)

    # Draw a line between the thumb and pinky tips
    h, w, _ = frame.shape
    pinky_coords = (
        int(pinky_tip.x * w),
        int(pinky_tip.y * h),
    )
    thumb_coords = (
        int(thumb_tip.x * w),
        int(thumb_tip.y * h),
    )
    cv2.line(frame, pinky_coords, thumb_coords, (0, 255, 0), 3)

while True:
    success, frame = capture.read()
    if not success:
        print("Failed to read from the camera.")
        break

    rgbFrame = frame[:, :, ::-1]  # Convert BGR to RGB
    results = hands.process(rgbFrame)

    # Draw FPS on the frame
    cv2.rectangle(frame, (0, 35), (650, 80), c_black, -1)
    drawFPS(frame)

    # Set motor direction
    ain1.write(1)  # Forward
    ain2.write(0)  # Reverse

    bin1.write(1)  # Forward
    bin2.write(0)  # Reverse

    # Normalize distance for PWM output (0 to 1) and write to motor pin
    pwm_value = min(max(dist_val / 100, 0), 1)  # Normalize to 0-1
    motorSpeedpin.write((pwm_value))
    motorSpeedpin2.write((pwm_value))
    print(dist_val)

    # Process hand landmarks if detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )
            drawLineTP(frame, hand_landmarks)

    # Show the video frame
    cv2.imshow("Ali Khan | Distance Thingy", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
capture.release()
cv2.destroyAllWindows()
board.exit()
