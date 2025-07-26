from kivy.app import App
from kivy.lang import Builder
from kivy.clock import mainthread
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, BooleanProperty
from androidstorage4kivy import Chooser, SharedStorage
from PIL import Image, ImageOps
import os
from jnius import autoclass
from android.storage import app_storage_path
import japanize_kivy
import threading
from datetime import datetime

# 明示的に .kv ファイルを読み込む
Builder.load_file('test.kv')

Uri = autoclass('android.net.Uri')

class MainLayout(BoxLayout):
	
	quality_jpeg = NumericProperty(85)
	quality_webp = NumericProperty(70)
	method_webp = NumericProperty(6)
	lossless_webp = BooleanProperty(False)
	
	def choose_image(self):
		
		self.ids.status.text = "準備完了"
		self.chooser = Chooser(self.on_sa_file_selected)
		self.chooser.choose_content('image/*', multiple=True)
	
	def choose_image_webp(self):
		
		self.ids.status.text = "準備完了"
		self.chooser = Chooser(self.on_sa_file_selected_webp)
		self.chooser.choose_content('image/*', multiple=True)
	
	def on_sa_file_selected(self, content_uris):
		
		self.ids.status.text = ""
		ss = SharedStorage()
		
		# 複数ファイルも考慮しループ
		def process_images():
			for uri in content_uris: # content_uris は Android の Uri オブジェクトのリスト
				selected_image = ss.copy_from_shared(uri) # アプリ側のプライベートストレージへファイルをコピー
				# 取得したファイルパスを got_selectionに
				self.got_selection([selected_image])
		
		
		threading.Thread(target=process_images, daemon=True).start()
		
	def on_sa_file_selected_webp(self, content_uris):
		self.ids.status.text = ""
		ss = SharedStorage()
		
		# 複数ファイルも考慮しループ
		def process_images_webp():
			for uri in content_uris:
				selected_image = ss.copy_from_shared(uri)
				# 取得したファイルパスを convert_webpに
				self.convert_webp([selected_image])
		
		threading.Thread(target=process_images_webp, daemon=True).start()
		
	
	@mainthread
	def update_status(self, message):
		self.ids.status.text += message
	
	def got_selection(self, selection):
		
		if not selection:
			self.update_status("画像が選択されませんでした")
			return
		
		input_image = selection[0]
		file_ext = os.path.splitext(input_image)[1].lower()
		
		if file_ext not in ('.png', '.jpg', '.jpeg'):
			self.update_status("'.png', '.jpg', '.jpeg'を選んでください")
			return
		
		app_dir = app_storage_path()
		output_path = os.path.join(app_dir, "resize")
		
		if not os.path.exists(output_path):
			os.makedirs(output_path)
		
		timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
		output_image = os.path.join(output_path, f"{timestamp}_small.jpg")
		
		try:
			img = Image.open(input_image)
			img = ImageOps.exif_transpose(img)
			
			width, height = img.size
			resized_img = img.resize((width // 2, height // 2))
			
			# 保存時の分岐
			if file_ext in ('.jpg', '.jpeg'):
				resized_img.save(output_image, format='JPEG', quality=self.quality_jpeg,
					optimize=True, subsampling=0)
			else:  # PNG の場合
				resized_img.save(output_image, format='PNG', optimize=True)
			
			ss = SharedStorage()
			shared = ss.copy_to_shared(private_file=output_image, collection=None ,filepath='resize/' + os.path.basename(output_image))
			
			if shared:
				os.remove(output_image)
				self.update_status(f"保存完了: Pictures/ImgCompressor/resize/{output_image}\n")
			else:
				self.update_status(f"保存に失敗しました: Pictures/ImgCompressor/resize/{output_image}\n")
			
		except Exception as e:
			self.update_status(f"保存に失敗しました: Pictures/ImgCompressor/resize/{output_image}\n")
	
	def convert_webp(self, selection):
		if not selection:
			self.update_status("画像が選択されませんでした")
			return
		
		input_image = selection[0]
		file_ext = os.path.splitext(input_image)[1].lower()
	
		if file_ext not in ('.png', '.jpg', '.jpeg'):
			self.update_status("'.png', '.jpg', '.jpeg'を選んでください")
			return
		
		app_dir = app_storage_path()
		output_path = os.path.join(app_dir, "webp")
		
		if not os.path.exists(output_path):
			os.makedirs(output_path)
		
		timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
		output_image = os.path.join(output_path, f"{timestamp}.webp")
		
		try:
			# 画像を開く
			img = Image.open(input_image).convert('RGB')
			img = ImageOps.exif_transpose(img)
			
			# WebP形式で保存\
			img.save(output_image, 'webp', quality=self.quality_webp, method=self.method_webp, optimize=True, lossless=self.lossless_webp)
			
			ss = SharedStorage()
			shared = ss.copy_to_shared(private_file=output_image, collection=None ,filepath='webp/' + os.path.basename(output_image))
			
			if shared:
				os.remove(output_image)
				self.update_status(f"保存完了: Pictures/ImgCompressor/webp/{output_image}\n")
			else:
				self.update_status(f"保存に失敗しました: Pictures/ImgCompressor/webp/{output_image}\n")
			
		except Exception as e:
			self.update_status(f"保存に失敗しました: Pictures/ImgCompressor/webp/{output_image}\n")
	

class ImgCompressorApp(App):
	def build(self):
		return MainLayout()

if __name__ == '__main__':
	ImgCompressorApp().run()