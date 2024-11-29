from tkinter import ttk
import tkinter as tk

class CustomerFrame(ttk.Frame):
    '''
    CustomerFrame主要是提供一個自訂的Frame,當使用者選取城市時
    必需要建立對應的CustomerFrame。
    CustomerFrame內會使用chechbox_widget,提供給使用者會勾選那一個站點
    '''
    def __init__(self,master=None,customers:list[str]=[],radio_controller=None,**kwargs):
        super().__init__(master=master, **kwargs)
        self.radion_controller = radio_controller
        #欄寬度的權重
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.selected_radio = tk.StringVar() #負責取得使用者選取的資料
        for idx,value in enumerate(customers):
            column = idx % 2
            index = int(idx / 2)
            print(idx,value)
            ttk.Radiobutton(self,
                            text=value,
                            value=value,
                            variable=self.selected_radio,
                            command=self.radio_button_selected).grid(column=column,row=index,sticky='w')
           
    
    def radio_button_selected(self):
        # Generate the custom event for the master widget
        self.event_generate("<<Radio_Button_Selected>>")
        print(f"Radio button selected: {self.selected_radio.get()}")  # Debugging