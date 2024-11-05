from tkinter import ttk 

class SitenameFrame(ttk.Frame):
    '''
    SitenameFrame主要是提供一個自訂的Frame,當使用者選取城市時
    必需要建立對應的SitenameFrame。
    SitenameFrame內會使用chechbox_widget,提供給使用者會勾選那一個站點
    '''
    def __init__(self,master=None,sitenames:list[str]=[],**kwargs):
        super().__init__(master=master, **kwargs)
        #欄寬度的權重
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        for idx,value in enumerate(sitenames):
            column = idx % 2
            index = int(idx / 2)
            print(idx,value)
            print(f'column:{column}')
            print(f'index:{index}')
            print("================")
