import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from datetime import datetime

class TestCaseCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("テストケース作成")
        self.root.geometry("400x500")  # 高さを増やす
        self.root.resizable(False, False)
        
        # テスト種類の選択
        self.test_type = tk.StringVar()
        test_types = ['単体テスト', '結合テスト', 'システムテスト']
        ttk.Label(root, text="テスト種類:").pack(pady=5)
        test_type_combo = ttk.Combobox(root, textvariable=self.test_type, values=test_types)
        test_type_combo.pack(pady=5)
        
        # ファイル選択ボタン
        ttk.Button(root, text="ファイル選択", command=self.select_file).pack(pady=10)
        
        # 選択されたファイルパスを表示
        file_frame = ttk.LabelFrame(root, text="選択されたファイル", padding=5)
        file_frame.pack(pady=5, padx=10, fill='x')
        self.file_path_label = ttk.Label(file_frame, text="", wraplength=350)
        self.file_path_label.pack(pady=5)
        
        # 処理分岐抽出ボタン
        ttk.Button(root, text="処理分岐抽出", command=self.extract_branches).pack(pady=10)
        
        # 処理分岐表示エリア
        branch_frame = ttk.LabelFrame(root, text="処理分岐", padding=5)
        branch_frame.pack(pady=5, padx=10, fill='both', expand=True)
        self.branch_text = scrolledtext.ScrolledText(branch_frame, height=10, wrap=tk.WORD)
        self.branch_text.pack(fill='both', expand=True)
        
        # テストケース作成ボタン
        ttk.Button(root, text="テストケース作成", command=self.create_test_case).pack(pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path_label.config(text=file_path)
            
    def analyze_file_content(self, file_path):
        """ファイルを解析して処理分岐を抽出"""
        branches = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for i, line in enumerate(lines, 1):
                    line = line.strip()
                    # 条件分岐の検出
                    if 'if ' in line or 'elif ' in line or 'else:' in line:
                        branches.append(f"行{i}: {line}")
                    # ループの検出
                    elif 'for ' in line or 'while ' in line:
                        branches.append(f"行{i}: {line}")
                    # 例外処理の検出
                    elif 'try:' in line or 'except ' in line or 'finally:' in line:
                        branches.append(f"行{i}: {line}")
        except Exception as e:
            print(f"ファイル解析エラー: {str(e)}")
        return branches

    def extract_branches(self):
        if not self.file_path_label.cget('text'):
            messagebox.showwarning("警告", "ファイルを選択してください")
            return
            
        try:
            branches = self.analyze_file_content(self.file_path_label.cget('text'))
            
            # テキストエリアをクリアして結果を表示
            self.branch_text.delete('1.0', tk.END)
            if branches:
                for branch in branches:
                    self.branch_text.insert(tk.END, f"■ {branch}\n")
            else:
                self.branch_text.insert(tk.END, "処理分岐が見つかりませんでした。")
                
        except Exception as e:
            messagebox.showerror("エラー", f"処理分岐の抽出中にエラーが発生しました:\n{str(e)}")

    def create_test_case(self):
        if not self.test_type.get():
            messagebox.showwarning("警告", "テスト種類を選択してください")
            return
            
        target_file = self.file_path_label.cget('text')
        if not target_file:
            messagebox.showwarning("警告", "ファイルを選択してください")
            return

        try:
            # 処理分岐を抽出
            branches = self.analyze_file_content(target_file)
            
            # ダウンロードフォルダのパスを取得
            downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"testcase_{self.test_type.get()}_{timestamp}.txt"
            file_path = os.path.join(downloads_path, filename)
            
            # テストケースファイルを作成
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"テスト種類: {self.test_type.get()}\n")
                f.write(f"対象ファイル: {target_file}\n")
                f.write(f"作成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("\n=== 処理分岐 ===\n")
                
                if branches:
                    for branch in branches:
                        f.write(f"\n■ {branch}\n")
                        f.write("前提条件:\n")
                        f.write("期待結果:\n")
                        f.write("確認項目:\n")
                        f.write("-" * 50 + "\n")
                else:
                    f.write("\n処理分岐が見つかりませんでした。\n")

            messagebox.showinfo("成功", f"テストケースを作成しました:\n{file_path}")

        except Exception as e:
            messagebox.showerror("エラー", f"テストケース作成中にエラーが発生しました:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TestCaseCreator(root)
    root.mainloop()
