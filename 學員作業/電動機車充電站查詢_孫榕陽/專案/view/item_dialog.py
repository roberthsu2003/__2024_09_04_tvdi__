import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import Dialog
from PIL import Image,ImageTk
import tkintermapview as tkmap

class MycustomDialog(Dialog):
    def __init__(self,parent,battery:list,title=None):
        
        
        self.lat=float(battery[4])
        self.lon=float(battery[5])
        super().__init__(parent=parent,title=title)

    def body(self, master):
  

        map_frame=ttk.Frame(master)
        map_widget=tkmap.TkinterMapView(map_frame,width=400,height=400,corner_radius=0)

        map_widget.set_position(self.lat,self.lon,marker=True)
        map_widget.set_zoom(15)
        map_widget.pack()
        map_frame.pack(padx=10,pady=10)

       


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

    
    def ok(self, event=None):
        # Override the ok method
        print("使用者按了ok")
        super().ok()
    
    def cancel(self, event= None) -> None:
        print("使用者按了cancel")
        super().cancel()