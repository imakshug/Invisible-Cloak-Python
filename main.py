import numpy as np
import cv2
import time

print("Starting Invisible Cloak...")
print("Make sure your cloak (red cloth) is not visible to the camera.")
print("Capturing background in 3 seconds...")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

time.sleep(3)
background_captured = False
for i in range(30):
    retval, back = cap.read()
    if retval:
        background_captured = True
back = np.flip(back, axis=1) if background_captured else None

if not background_captured:
    print("Error: Could not capture background.")
    cap.release()
    exit()

print("Background captured. You can now use your cloak!")

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        break
    img = np.flip(img, axis=1)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Detect red color in HSV
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)

    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2

    # Remove noise from mask
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

    # Replace cloak area with background
    img[np.where(mask == 255)] = back[np.where(mask == 255)]

    cv2.imshow("Harry Potter's Invisible Cloak", img)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()