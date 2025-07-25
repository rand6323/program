import os
from PIL import Image

# 画像が保存されているディレクトリ
input_directory = 'input_img/'
output_directory = 'output_img/'

# 出力ディレクトリが存在しない場合は作成
if not os.path.exists(output_directory):
	os.makedirs(output_directory)

# ディレクトリ内のすべての画像ファイルを処理
for filename in os.listdir(input_directory):

	file_ext = os.path.splitext(filename)[1].lower()
	
	if file_ext not in ('.png', '.jpg', '.jpeg'):
		continue
	
	input_path = os.path.join(input_directory, filename)
	output_path = os.path.join(output_directory, filename)
	
	try:
		with Image.open(input_path) as img:
			
			# 元の幅と高さを取得
			width, height = img.size
			
			# 新しいサイズを計算（50%）
			new_size = (width // 2, height // 2)
			
			# 画像をリサイズ
			resized_img = img.resize(new_size)
			
			# 保存時の分岐
			if file_ext in ('.jpg', '.jpeg'):
				resized_img.save(output_path, format='JPEG', quality=85,
					optimize=True, subsampling=0)
			else:  # PNG の場合
				resized_img.save(output_path, format='PNG', optimize=True)
			
			print(f'リサイズ成功: {input_path} → {output_path}')
			
	except Exception as e:
		print(f'エラー: {input_path} の処理中にエラーが発生しました。詳細: {e}')