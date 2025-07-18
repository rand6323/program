import cv2

# 学習済みモデルと顔検出器の読み込み
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("./models/face_recognizer.yml")
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# ラベルと名前の対応付け
names = {0: "MyFace"}  # ラベル0がこの自分だけとします

# カメラ起動
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("リアルタイム認識中。ESCキーで終了します。")
while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1,
                                          minNeighbors=5, minSize=(60, 60))

    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        label, confidence = recognizer.predict(face_roi)

        if confidence < 80:
            text = f"{names.get(label,'?')} ({confidence:.1f})"
            color = (0, 255, 0)
        else:
            text = f"Unknown ({confidence:.1f})"
            color = (0, 0, 255)

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow('Real-Time Face Recognition', frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESCキーで終了
        break

cap.release()
cv2.destroyAllWindows()
