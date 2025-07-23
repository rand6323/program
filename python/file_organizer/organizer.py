import os
import shutil
import logging
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime

# 拡張子カテゴリ定義
EXT_OPTIONS = {
    '.jpg': '画像', '.jpeg': '画像', '.png': '画像',
    '.txt': '文書', '.pdf': '文書', '.docx': '文書', '.xlsx': '文書',
    '.mp3': '音楽', '.wav': '音楽', '.mp4': '動画',
}

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ファイル整理アプリ")
        self.root.geometry("450x500")
        self.folder_path = ''

        # UI構成
        tk.Button(root, text="フォルダ選択", command=self.select_folder).pack(pady=5)
        self.folder_label = tk.Label(root, text="未選択")
        self.folder_label.pack()

        tk.Label(root, text="拡張子を選択").pack()
        self.ext_vars = {ext: tk.BooleanVar(value=True) for ext in EXT_OPTIONS}
        for ext, var in self.ext_vars.items():
            tk.Checkbutton(root, text=ext, variable=var).pack(anchor='w')

        # 日付ソース選択
        self.date_source = tk.StringVar(value='mtime')
        frame = tk.Frame(root); frame.pack(pady=5)
        tk.Radiobutton(frame, text="更新日時", variable=self.date_source, value='mtime').pack(side='left')
        tk.Radiobutton(frame, text="作成日時", variable=self.date_source, value='ctime').pack(side='left')

        self.subfolder_var = tk.BooleanVar(value=False)
        tk.Checkbutton(root, text="年→年＋月フォルダ", variable=self.subfolder_var).pack(pady=5)

        # 進捗表示
        self.progress = ttk.Progressbar(root, length=300)
        self.progress.pack(pady=5)
        self.status_label = tk.Label(root, text="")
        self.status_label.pack()

        tk.Button(root, text="整理開始", command=self.organize_files).pack(pady=10)

        # ログ設定
        logging.basicConfig(filename='organizer.log',
                            level=logging.INFO,
                            format='%(asctime)s %(levelname)s %(message)s')

    def select_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_path = path
            self.folder_label.config(text=path)

    def organize_files(self):
        if not self.folder_path:
            return messagebox.showwarning("警告", "フォルダを選択してください")
        exts = [e for e, v in self.ext_vars.items() if v.get()]
        if not exts:
            return messagebox.showwarning("警告", "拡張子を1つ以上選択してください")

        files = [f for f in os.listdir(self.folder_path)
                 if os.path.isfile(os.path.join(self.folder_path, f))
                 and os.path.splitext(f)[1].lower() in exts]
        total = len(files)
        if total == 0:
            return messagebox.showinfo("Info", "対象ファイルはありません")

        self.progress['maximum'] = total
        self.progress['value'] = 0

        for idx, file in enumerate(files, 1):
            self.status_label.config(text=f"{idx}/{total}: {file}")
            self.root.update_idletasks()

            full = os.path.join(self.folder_path, file)
            ts = os.path.getmtime(full) if self.date_source.get() == 'mtime' else os.path.getctime(full)
            dt = datetime.fromtimestamp(ts)
            year, ym = dt.strftime('%Y'), dt.strftime('%Y%m')

            target = os.path.join(self.folder_path, year)
            if self.subfolder_var.get():
                target = os.path.join(target, ym)
            category = EXT_OPTIONS.get(os.path.splitext(file)[1].lower(), 'その他')
            target = os.path.join(target, category)
            os.makedirs(target, exist_ok=True)

            dest = os.path.join(target, file)
            base, ext = os.path.splitext(file)
            i = 1
            while os.path.exists(dest):
                dest = os.path.join(target, f"{base}_{i}{ext}")
                i += 1

            shutil.move(full, dest)
            logging.info(f"Moved: {full} → {dest}")

            self.progress['value'] = idx

        messagebox.showinfo("完了", "整理が完了しました！")
        self.status_label.config(text="完了")

if __name__ == '__main__':
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()
