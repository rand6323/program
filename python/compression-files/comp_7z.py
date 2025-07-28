import os
import sys
import re
import py7zr

def compressor_7z(src_dir='./work_dir', zip_path='./output_dir/work_dir.7z', password=None):
	
	# 圧縮時の設定
	# id      圧縮方式
	# preset  圧縮レベル 数値が大きいほど圧縮率は高いが処理時間も増える
	
	filters = [{'id': py7zr.FILTER_LZMA2, 
				'preset': 6}]
	
	kwargs = {'filters': filters}
	
	if password:
		# パスワードに使用できる文字は後述のエラー文のとおり
		pattern = re.compile(r'^[ -~]+$')
		
		if not pattern.match(password):
			raise ValueError("パスワードには以下の文字のみ使用できます：\n" +
							"- 英字（A～Z、a～z）数字（0～9）\n" +
							"! \" # $ % & ' ( ) * + , - . / : ; < = > ? @ [ \\ ] ^ _ ` { | } ~（スペースも可）\n" +
							"ドット「.」やスラッシュ「/」も含まれます。")
		
		kwargs['password'] = password
	
	
	# 暗号付き7zの生成
	with py7zr.SevenZipFile(zip_path, 'w', **kwargs) as archive:
		
		if password:
			archive.set_encrypted_header(True)
		
		archive.writeall(src_dir)

if __name__ == '__main__':
	
	# python comp_7z.py abcd1234
	# と入力すると、「abcd1234」がパスワードに設定される
	# python comp_7z.pyのみ入力した場合はパスワード設定なし
	
	pwd = None
	args = sys.argv
	
	if len(args) >= 2:
		if args[1]:
			pwd = args[1]
	
	compressor_7z(password=pwd)