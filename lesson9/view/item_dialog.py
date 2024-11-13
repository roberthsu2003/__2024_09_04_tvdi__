import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import Dialog
from PIL import Image, ImageTk

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
        canvas_left = tk.Canvas(main_frame,width=200,height=200)
        canvas_left.create_rectangle(10,10,190,190,outline="#9E7A7A",width=2)
        canvas_left.create_text(100, 40, text=f'AQI:{self.status}',font=("Helvetica",24,"bold"),fill='#9E7A7A')
        #canvas_left.create_oval(70, 70, 130, 130, outline="#f11",fill="#1f1", width=2)
        self.img = Image.open("./images/green.png")
        #self.resize_image = img.resize((60,60))
        self.green = ImageTk.PhotoImage(self.img)
        canvas_left.create_image(100, 100, anchor='center', image=self.green)      
        canvas_left.pack(side='left')

        canvas_right = tk.Canvas(main_frame,width=200,height=200)
        canvas_right.create_oval(10, 10, 80, 80, outline="#f11",fill="#1f1", width=2)
        canvas_right.create_text(200, 150, text=self.status,font=("Helvetica",24,"bold"),fill='#9E7A7A')
        canvas_right.pack(side='right')
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

        

