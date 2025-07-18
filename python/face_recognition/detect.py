import cv2
import os

# 入力ディレクトリと出力ディレクトリのパス
input_dir = "./input"
output_dir = "./detected"

# 出力ディレクトリが存在しない場合は作成
os.makedirs(output_dir, exist_ok=True)

# 顔のカスケード分類器を読み込む
cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(cascade_path)
if face_cascade.empty():
    print("読み込みに失敗しました:", cascade_path)
else:
    print("Haarcascade 読み込み成功:", cascade_path)

# 入力ディレクトリ内のすべての画像ファイルを処理
for filename in os.listdir(input_dir):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        img_path = os.path.join(input_dir, filename)
        img = cv2.imread(img_path)
        if img is None:
            print(f"{filename} の読み込みに失敗しました。")
            continue

        # 画像をグレースケールにする
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 顔検出を実行
        faces = face_cascade.detectMultiScale(gray)
        if len(faces) == 0:
            print(f"{filename} で顔が検出されませんでした。")
            continue

        # 顔部分に矩形を描画し、切り出して保存
        for i, (x, y, w, h) in enumerate(faces):
            # 顔部分を切り出し
            face_crop = img[y:y+h, x:x+w]
            # 顔部分を保存
            face_filename = f"{os.path.splitext(filename)[0]}_crop.jpg"
            face_path = os.path.join(output_dir, face_filename)
            cv2.imwrite(face_path, face_crop)
            print(f"{face_filename} を保存しました。")
