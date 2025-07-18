import cv2
import os
import numpy as np

# 入力ディレクトリのパス
input_dir = "./input"

# 顔認識モデルの初期化
recognizer = cv2.face.LBPHFaceRecognizer_create()

# データとラベルの準備
faces = []
labels = []
label = 0  # この1人だけのラベル

# 顔検出用のHaar Cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

for filename in os.listdir(input_dir):
    if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue
    img_path = os.path.join(input_dir, filename)
    img = cv2.imread(img_path)
    if img is None:
        print(f"{filename} の読み込みに失敗しました")
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)  # 明暗の均一化を加えると検出率向上

    faces_detected = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    if len(faces_detected) == 0:
        print(f"{filename}：顔が検出されませんでした")
    else:
        for (x, y, w, h) in faces_detected:
            face = gray[y:y+h, x:x+w]
            faces.append(face)
            labels.append(label)
        print(f"{filename} で {len(faces_detected)} 枚の顔を抽出")

print(f"合計顔画像数: {len(faces)}, ラベル数: {len(labels)}")

assert len(faces) == len(labels) and len(faces) > 1, "学習データ不足か対応ズレがあります"

# LBPHで学習
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(faces, np.array(labels))
recognizer.save("./models/face_recognizer.yml")
print("学習完了しました")
