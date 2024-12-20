from tkinter.simpledialog import Dialog
from tkinter import ttk
from tkinter import Misc
import tkinter as tk

class CustomMessagebox(Dialog):    
    def __init__(self, parent:Misc, title:str,name:str,bmi:float,status:str,advice:str,status_color:str):        
        self.parent = parent
        self.name = name
        self.bmi = bmi
        self.status = status
        self.advice = advice
        style = ttk.Style()
        style.configure('status.TLabel',foreground=status_color)
        super().__init__(parent=parent, title=title)

    def body(self, master):
      
        contain_frame = ttk.Frame(master,style='Input.TFrame')
      
        label_name = ttk.Label(contain_frame, text="姓名:")
        label_name.grid(row=0, column=0, padx=10, pady=10,sticky=tk.E)

        self.value_name = ttk.Label(contain_frame,text=self.name)
        self.value_name.grid(row=0, column=1, padx=10, pady=10)

       
        label_bmi = ttk.Label(contain_frame, text="BMI值:")
        label_bmi.grid(row=1, column=0, padx=10, pady=10,sticky=tk.E)

        self.value_height = ttk.Label(contain_frame,text=f'{self.bmi:.2f}')
        self.value_height.grid(row=1, column=1, padx=10, pady=10)

        
        label_status = ttk.Label(contain_frame, text="狀態:")
        label_status.grid(row=2, column=0, padx=10, pady=10,sticky=tk.E)

        self.value_status = ttk.Label(contain_frame,text=self.status,style='status.TLabel')
        self.value_status.grid(row=2, column=1, padx=10, pady=10)

       
        label_advice = ttk.Label(contain_frame, text="建議:")
        label_advice.grid(row=3, column=0, padx=10, pady=10,sticky=tk.E)

        self.value_advice = ttk.Label(contain_frame,text=self.advice)
        self.value_advice.grid(row=3, column=1, padx=10, pady=10)   

        contain_frame.pack(pady=50,padx=100)

    def apply(self):
        
        self.parent.name_value.set('')
        self.parent.hight_value.set('')
        self.parent.weight_value.set('')

    def buttonbox(self):
       
        box = ttk.Frame(self)
        self.ok_button = tk.Button(box, text="確定", width=10, command=self.ok, default=tk.ACTIVE)
        self.ok_button.pack(side=tk.LEFT, padx=10, pady=10)
        box.pack()

    def ok(self):
       
        print("OK button was clicked!")
        super().ok()


    