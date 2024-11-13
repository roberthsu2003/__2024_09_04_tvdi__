import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import Dialog

class MyCustomDialog(Dialog):
    def __init__(self,parent,record:list,title=None):
        self.date = record[0]
        self.county = record[1]
        self.sitename = record[2]
        self.aqi=record[3]
        self.pm25 = record[4]
        self.status = record[5]
        self.lat = float(record[6])
        self.lon = float(record[7])
        super().__init__(parent=parent,title=title)

    def body(self, master):
        # 創建對話框主體。返回應具有初始焦點的控件。
        main_frame = ttk.Frame(master,borderwidth=1,relief='groove')
        ttk.Label(main_frame,text=self.status).pack()
        canvas = tk.Canvas(main_frame,width=400,height=400)
        canvas.create_oval(10, 10, 80, 80, outline="#f11",fill="#1f1", width=2)
        canvas.pack()
        main_frame.pack(expand=True,fill='x')

    def apply(self):
        # 當用戶按下確定時處理數據
        print("使用者按了apply")

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

        

