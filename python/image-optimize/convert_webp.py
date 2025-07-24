import os
from PIL import Image

# 画像が保存されているディレクトリ
input_directory = 'input_img/'
output_directory = 'output_img/'

# 出力ディレクトリが存在しない場合は作成
if not os.path.exists(output_directory):
	os.makedirs(output_directory)

# 入力フォルダ内のすべての画像ファイルを処理
for filename in os.listdir(input_directory):
	input_path = os.path.join(input_directory, filename)
	if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
		try:
			# 画像を開く
			img = Image.open(input_path).convert('RGB')
			
			# 出力ファイル名を生成
			output_path = os.path.join(output_directory, f'{os.path.splitext(filename)[0]}.webp')
			
			# WebP形式で保存（品質は50）
			img.save(output_path, 'webp', quality=50)
			
			print(f'変換成功: {input_path} -> {output_path}')
			
		except Exception as e:
			print(f'エラー: {input_path} の処理中にエラーが発生しました。詳細: {e}')