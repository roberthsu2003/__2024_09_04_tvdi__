import tkinter as tk
from tkinter.simpledialog import Dialog

class MyCustomDialog(Dialog):
    def __init__(self,parent,record:list,title=None):
        print(f'傳過來的資料:{record}')
        super().__init__(parent=parent,title=title)

    def body(self, master):
        # 創建對話框主體。返回應具有初始焦點的控件。
        tk.Label(master, text="請輸入你的名字:").grid(row=0)
        self.name_entry = tk.Entry(master)
        self.name_entry.grid(row=0, column=1)
        return self.name_entry
    
    def apply(self):
        # 當用戶按下確定時處理數據
        print("使用者按了apply")
        self.result = self.name_entry.get()

    def buttonbox(self):
        # Add custom buttons (overriding the default buttonbox)
        box = tk.Frame(self)
        self.ok_button = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        self.ok_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.cancel_button = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        self.cancel_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack()

    def ok(self,event=None):
        print("使用者按了ok")
        super().ok()

    def cancel(self,evnet=None):
        print("使用者按下cancel")
        super().cancel()

        

