from tkinter import ttk
import tkinter as tk

class SitenameFrame(ttk.Frame):
    '''
    SitenameFrame主要是提供一個自訂的Frame,當使用者選取城市時
    必需要建立對應的SitenameFrame。
    SitenameFrame內會使用chechbox_widget,提供給使用者會勾選那一個站點
    '''
    def __init__(self,master=None,sitenames:list[str]=[],radio_controller=None,**kwargs):
        super().__init__(master=master, **kwargs)
        self.radion_controller = radio_controller
        #欄寬度的權重
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.selected_radio = tk.StringVar() #負責取得使用者選取的資料
        for idx,value in enumerate(sitenames):
            column = idx % 2
            index = int(idx / 2)
            print(idx,value)
            ttk.Radiobutton(self,
                            text=value,
                            value=value,
                            variable=self.selected_radio,
                            command=self.radio_button_selected).grid(column=column,row=index,sticky='w')
           
    
    def radio_button_selected(self):
        if self.radion_controller != None:
            self.radion_controller(self.selected_radio.get())
