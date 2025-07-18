import cv2, os

cap = cv2.VideoCapture(0)
os.makedirs('input', exist_ok=True)
count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow("Capture - press 'c' to save, 'q' to quit", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        cv2.imwrite(f"input/face_{count:03d}.jpg", frame)
        print(f"Saved input/face_{count:03d}.jpg")
        count += 1
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
