import tkinter as tk
from tkinter.simpledialog import Dialog
from tkinter import ttk


class LoginDialog(Dialog):
    def __init__(self, parent, title=None):
        self.parent = parent
        super().__init__(parent=parent, title=title)

    def body(self, master):
        self.title('誰想看電影?')
        
        # ====Style===      
        style = ttk.Style(self)
        style.configure('TopFrame.TLabel', font=('Arial', 20))
        # ====End Style===

        # ====TOP Frame====
        top_frame = ttk.Frame(master, style='TopFrame.TLabel')
        ttk.Label(top_frame, text='Please Log in', style='TopFrame.TLabel').pack()
        top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # ====End TOP Frame====

        # ====Bottom Frame====
        bottom_frame = ttk.Frame(master)
        
        # ====Login =====
        ttk.Label(bottom_frame, text='User Name').grid(row=0, column=0, pady=10)
        ttk.Label(bottom_frame, text='Password').grid(row=1, column=0, pady=10)

        bottom_frame.columnconfigure(index=0, weight=1)
        bottom_frame.columnconfigure(index=1, weight=9)

        self.username = tk.StringVar()
        ttk.Entry(bottom_frame, textvariable=self.username).grid(row=0, column=1, sticky='E')

        self.password = tk.StringVar()
        ttk.Entry(bottom_frame, textvariable=self.password, show='*').grid(row=1, column=1, sticky='E')

        bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        return bottom_frame  # 必須返回第一個獲得焦點的小部件的父框架

    def apply(self):
        """當用戶點擊確定按鈕時調用"""
        # 在這裡處理登入邏輯
        username = self.username.get()
        password = self.password.get()
        
        # 這裡添加您的登入驗證邏輯
        if self.validate_login(username, password):
            self.parent.deiconify()  # 顯示主視窗
            return True
        return False

    def validate_login(self, username, password):
        """驗證登入資訊"""
        # 這裡添加您的驗證邏輯
        # 示例：假設用戶名為 "admin"，密碼為 "password"
        return username == "1234" and password == "5678"

    def buttonbox(self):
        """自定義按鈕框"""
        box = ttk.Frame(self)

        w = ttk.Button(box, text="登入", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = ttk.Button(box, text="取消", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()