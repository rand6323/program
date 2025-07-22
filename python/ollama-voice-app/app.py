from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import requests
import os
import subprocess
import time
import threading
import uuid # ユニークなファイル名を生成するため
import glob # 一時ファイル削除のため
import ollama
from config import Config
from voices import VOICEVOX_SPEAKERS
import json

CONFIG_PATH = "config.json"

OLLAMA_API_URL = 'http://localhost:11434/api'
ollama_model_cache = None

# VOICEVOXの設定
VOICEVOX_API_URL = "http://127.0.0.1:50021"
VOICEVOX_PATH = os.getenv("VOICEVOX_PATH", r"C:\path\to\VOICEVOX.exe") # ユーザー環境変数で変数名に VOICEVOX_PATH、変数値に C:\path\to\VOICEVOX.exe を設定する

# 一時音声ファイルを保存するディレクトリ
AUDIO_TEMP_DIR = "audio_temp"
os.makedirs(AUDIO_TEMP_DIR, exist_ok=True) # ディレクトリがなければ作成

chat_history = []

def load_settings():
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
            app.config.update(json.load(f))
    else:
        save_settings()

def save_settings():
    data = {
        'OLLAMA_MODEL': app.config.get('OLLAMA_MODEL', ''),
        'VOICEVOX_SPEAKER_ID': app.config['VOICEVOX_SPEAKER_ID'],
        'VOICEVOX_SPEED': app.config['VOICEVOX_SPEED'],
        'VOICEVOX_PITCH': app.config['VOICEVOX_PITCH'],
        'VOICEVOX_INTONATION': app.config['VOICEVOX_INTONATION'],
    }
    with open(SETTINGS_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def reload_ollama_models():
    global ollama_model_cache
    ollama_model_cache = None

def list_ollama_models():
    global ollama_model_cache
    if ollama_model_cache is not None:
        return ollama_model_cache  # キャッシュがあればそれを返す

    try:
        resp = requests.get(f"{OLLAMA_API_URL}/tags")
        resp.raise_for_status()
        ollama_model_cache = [m['model'] for m in resp.json().get('models', [])]
        return ollama_model_cache
    except Exception as e:
        print("Ollama モデル取得エラー:", e)
        return []

def start_ollama():
    try:
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=False
        )
        print("Ollama サーバーをバックグラウンドで起動しました。")
    except Exception as e:
        print(f"Ollama 起動エラー: {e}")

def load_settings():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            data = json.load(f)
            app.config.update(data)

def save_settings():
    data = {
        'VOICEVOX_SPEAKER_ID': app.config['VOICEVOX_SPEAKER_ID'],
        'VOICEVOX_SPEED': app.config['VOICEVOX_SPEED'],
        'VOICEVOX_PITCH': app.config['VOICEVOX_PITCH'],
        'VOICEVOX_INTONATION': app.config['VOICEVOX_INTONATION'],
        'OLLAMA_MODEL': app.config.get('OLLAMA_MODEL', '')
    }
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=2)

app = Flask(__name__)
app.config.from_object(Config)
load_settings()  # 保存済み設定があれば上書き

@app.route('/')
def index():
    """
    チャット画面の初期表示
    """
    return render_template('index.html')

@app.template_filter('format_number')
def format_number_filter(value, digits=2):
    try:
        return f"{float(value):.{digits}f}"
    except (ValueError, TypeError):
        return value

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    models = list_ollama_models()  # Ollamaモデル一覧取得
    load_settings()

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'model':
            model_name = request.form.get('model_name')
            if model_name:
                app.config['OLLAMA_MODEL'] = model_name
                save_settings()
        elif action == 'voice':
            try:
                app.config['VOICEVOX_SPEAKER_ID'] = int(request.form.get('speaker_id'))
                app.config['VOICEVOX_SPEED'] = float(request.form.get('speed'))
                app.config['VOICEVOX_PITCH'] = float(request.form.get('pitch'))
                app.config['VOICEVOX_INTONATION'] = float(request.form.get('intonation'))
                save_settings()
            except (TypeError, ValueError):
                # フォーム値が不正の場合は何もしないかエラー処理を
                pass

        return redirect(url_for('settings'))

    return render_template('settings.html',
                           models=models,
                           model_selected=app.config.get('OLLAMA_MODEL', models[0] if models else ''),
                           speaker_id=app.config['VOICEVOX_SPEAKER_ID'],
                           speakers=VOICEVOX_SPEAKERS,
                           speed=f"{app.config['VOICEVOX_SPEED']:.2f}",
                           pitch=f"{app.config['VOICEVOX_PITCH']:.2f}",
                           intonation=f"{app.config['VOICEVOX_INTONATION']:.2f}",
                           )

@app.route('/send_message', methods=['POST'])
def send_message():
    global chat_history  # 明示的にグローバル履歴を使う

    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"reply": "メッセージが空です。"}), 400

    bot_reply_full = ""
    audio_file_path = None

    try:
        # ユーザー入力を履歴に追加
        chat_history.append({"role": "user", "content": user_message})

        # Ollamaへ履歴を含めて問い合わせ
        ollama_stream = ollama.chat(
            model='gemma3:4b',
            messages=chat_history,
            stream=True,
        )

        # 応答を逐次受け取って連結
        for chunk in ollama_stream:
            content = chunk['message']['content']
            bot_reply_full += content

        # 応答を履歴に追加
        chat_history.append({"role": "assistant", "content": bot_reply_full})

        # 完全な応答ができたので、VOICEVOXで音声を生成
        audio_file_name = f"{uuid.uuid4()}.wav"
        audio_file_path = os.path.join(AUDIO_TEMP_DIR, audio_file_name)

        # 1. 音声合成クエリの生成
        params_query = {
          'text': bot_reply_full,
          'speaker': app.config['VOICEVOX_SPEAKER_ID']
        }
        response_query = requests.post(f"{VOICEVOX_API_URL}/audio_query", params=params_query)
        response_query.raise_for_status()
        audio_query = response_query.json()

        # ここで音声合成クエリのパラメータを調整
        audio_query['speedScale']     = app.config['VOICEVOX_SPEED']
        audio_query['pitchScale']     = app.config['VOICEVOX_PITCH']
        audio_query['intonationScale'] = app.config['VOICEVOX_INTONATION']
        audio_query['volumeScale']    = app.config.get('VOICEVOX_VOLUME', 1.0)

        # 2. 音声の生成
        params_synthesis = {'speaker': app.config['VOICEVOX_SPEAKER_ID']}
        headers_synthesis = {'Content-Type': 'application/json'}
        response_synthesis = requests.post(
            f"{VOICEVOX_API_URL}/synthesis",
            headers=headers_synthesis,
            params=params_synthesis,
            json=audio_query
        )
        response_synthesis.raise_for_status()

        # 生成された音声データを一時ファイルに保存
        with open(audio_file_path, "wb") as f:
            f.write(response_synthesis.content)

        # Flaskの返り値として、完全なテキストと音声URLを返す
        return jsonify({
            "reply": bot_reply_full,
            "audio_url": f"/get_audio?file={audio_file_name}" if audio_file_path else None
        })

    except requests.exceptions.ConnectionError:
        error_message = "VOICEVOXが起動していないか、APIが有効になっていません。"
        print(error_message)
        return jsonify({"reply": bot_reply_full + f" ({error_message})", "audio_url": None})
    except requests.exceptions.RequestException as e:
        error_message = f"VOICEVOX APIエラー: {e}"
        print(error_message)
        return jsonify({"reply": bot_reply_full + f" ({error_message})", "audio_url": None})
    except Exception as e:
        error_message = f"予期せぬエラー: {e}"
        print(error_message)
        return jsonify({"reply": bot_reply_full + f" ({error_message})", "audio_url": None})

@app.route('/get_audio')
def get_audio():
    """
    生成された音声ファイルをブラウザに返すAPIエンドポイント
    """
    file_name = request.args.get('file')
    file_path = os.path.join(AUDIO_TEMP_DIR, file_name)

    if file_path and os.path.exists(file_path):
        # ファイルを送信後、別スレッドで削除処理をキューに入れる
        # すぐに削除するとファイルが読み込まれる前に消えてしまう可能性があるため
        threading.Thread(target=delete_audio_file_delayed, args=(file_path,)).start()
        return send_file(file_path, mimetype='audio/wav')
    return "File not found", 404

def delete_audio_file_delayed(file_path, delay=5):
    """
    指定されたファイルを一定時間後に削除する関数
    """
    time.sleep(delay) # ブラウザがファイルを読み込むのに十分な時間を確保
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"一時音声ファイル '{file_path}' を削除しました。")
    except Exception as e:
        print(f"一時音声ファイルの削除中にエラーが発生しました: {e}")

def start_voicevox_and_wait_for_api():
    """
    VOICEVOXアプリケーションをGPUでバックグラウンド起動し、APIが利用可能になるまで待機する関数
    """
    print("VOICEVOXをGPUでバックグラウンド起動しています...")
    try:
        # VOICEVOXの実行コマンドと引数
        # GPUモードとWeb APIモードで起動
        command = [VOICEVOX_PATH, "--gpu", "--cmd"]

        # Windowsの場合のみ、コンソールウィンドウを表示しないフラグを設定
        creation_flags = 0
        if os.name == 'nt': # Windowsの場合
            creation_flags = subprocess.CREATE_NO_WINDOW

        # Popenを使ってVOICEVOXを非同期で起動
        # shell=False (デフォルト) を明示的に指定することで、より安全にプロセスを起動
        subprocess.Popen(command, creationflags=creation_flags)
        print("VOICEVOXを起動しました。APIの準備を待機中...")

        # VOICEVOX APIが利用可能になるまでポーリングで確認
        max_retries = 30 # 最大30回リトライ (30 * 1秒 = 30秒)
        for i in range(max_retries):
            try:
                response = requests.get(f"{VOICEVOX_API_URL}/speakers") # スピーカーリスト取得でAPI稼働確認
                if response.status_code == 200:
                    print("VOICEVOX APIが利用可能です。")
                    return True
            except requests.exceptions.ConnectionError:
                pass # まだ接続できない
            print(f"VOICEVOX API接続試行中... ({i+1}/{max_retries})")
            time.sleep(1) # 1秒待機
        print("エラー: VOICEVOX APIが指定時間内に利用可能になりませんでした。手動で起動・確認してください。")
        return False
    except FileNotFoundError:
        print(f"エラー: VOICEVOX実行ファイルが見つかりません。パスを確認してください: {VOICEVOX_PATH}")
        return False
    except Exception as e:
        print(f"VOICEVOX起動中に予期せぬエラーが発生しました: {e}")
        return False

# Flaskアプリケーション起動前に一時ファイルをすべてクリーンアップ
def clean_old_audio_files():
    files = glob.glob(os.path.join(AUDIO_TEMP_DIR, "*.wav"))
    for f in files:
        try:
            os.remove(f)
            print(f"起動時に古い一時ファイル '{f}' を削除しました。")
        except Exception as e:
            print(f"起動時のファイル削除中にエラー: {e}")

if __name__ == '__main__':
    # 古い一時ファイルを削除
    clean_old_audio_files()

    # Flaskサーバー起動前にVOICEVOXを別スレッドで起動
    voicevox_thread = threading.Thread(target=start_voicevox_and_wait_for_api)
    voicevox_thread.daemon = True # メインスレッド終了時に一緒に終了
    voicevox_thread.start()
    
    # Ollama 起動（非同期）
    start_ollama()

    app.run(debug=True, port=5000, host='0.0.0.0')