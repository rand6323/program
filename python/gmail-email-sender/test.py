import os
import base64
import mimetypes
from email.message import EmailMessage

# Gmail APIを利用
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Gmail APIのスコープ
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def send_any_attachment(to, subject, body, filepaths, sender="example@gmail.com"):
	
	# 取得したtoken.jsonを使用
	if os.path.exists("token.json"):
		creds = Credentials.from_authorized_user_file("token.json", SCOPES)
	
	# token.jsonが存在しない場合、トークンを取得
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
			creds = flow.run_local_server(port=0)
		# 取得したcredentialsをJSON形式で保存
		with open("token.json", "w") as token:
			token.write(creds.to_json())
	
	service = build('gmail', 'v1', credentials=creds)
	
	# メールを作成
	msg = EmailMessage()
	msg['From'] = sender
	msg['To'] = to
	msg['Subject'] = subject
	
	# 本文を作成
	msg.set_content(body)
	
	# 複数ファイルをループで添付
	for filepath in filepaths:
		
		# ファイル拡張子からデータの種類を推定
		# 推定できない場合はapplication/octet-streamを設定
		ctype, encoding = mimetypes.guess_type(filepath)
		if ctype is None or encoding:
			maintype, subtype = 'application', 'octet-stream'
		else:
			maintype, subtype = ctype.split('/', 1)
		
		
		with open(filepath, 'rb') as f:
			data = f.read()
		filename = os.path.basename(filepath)
		
		# メールの添付部分を作成
		msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=filename)
	
	# 作成したメールをGmailAPIが扱える形式に変換する
	raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
	
	# メール送信を実行
	# userId="me"は認証ユーザーのGmailアカウントを示す
	return service.users().messages().send(userId="me", body={'raw': raw}).execute()
	
# 使用例
# 添付ファイルは複数記載してもよい
result = send_any_attachment(
	to="test@gmail.com",
	subject="添付ファイル付きメール",
	body="複数のファイルを添付しています。",
	filepaths=["sample1.pdf", "sample2.jpg", "sample3.txt"]
)
print("Sent message ID:", result['id'])
