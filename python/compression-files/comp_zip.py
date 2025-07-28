import os
import sys
import re
import pyzipper

# ZIP圧縮
def compressor_zip(src_dir='./work_dir', zip_path='./output_dir/work_dir.zip', password=None):
	
	# 圧縮時の設定
	# compression    ZIP圧縮方式
	# compresslevel  圧縮レベル 数値が大きいほど圧縮率は高いが処理時間も増える
	
	mode_args = {
		'compression': pyzipper.ZIP_DEFLATED,
		'compresslevel': 6,
	}
	
	if password:
		# パスワードに使用できる文字は後述のエラー文のとおり
		pattern = re.compile(r'^[ -~]+$')
		
		if not pattern.match(password):
			raise ValueError("パスワードには以下の文字のみ使用できます：\n" +
							"- 英字（A～Z、a～z）数字（0～9）\n" +
							"! \" # $ % & ' ( ) * + , - . / : ; < = > ? @ [ \\ ] ^ _ ` { | } ~（スペースも可）\n" +
							"ドット「.」やスラッシュ「/」も含まれます。")
		
		mode_args['encryption'] = pyzipper.WZ_AES
	
	# 暗号付きZIPの生成
	with pyzipper.AESZipFile(zip_path, 'w', **mode_args) as zf:
		
		if password:
			zf.setpassword(password.encode())
		
		# サブディレクトリも含める
		for root, _, files in os.walk(src_dir):
			for fname in files:
				full = os.path.join(root, fname)
				archive = os.path.relpath(full, start=src_dir)
				zf.write(full, arcname=archive)

if __name__ == '__main__':
	
	# python comp_zip.py abcd1234
	# と入力すると、「abcd1234」がパスワードに設定される
	# python comp_zip.pyのみ入力した場合はパスワード設定なし
	
	pwd = None
	args = sys.argv
	
	if len(args) >= 2:
		if args[1]:
			pwd = args[1]
	
	compressor_zip(password=pwd)