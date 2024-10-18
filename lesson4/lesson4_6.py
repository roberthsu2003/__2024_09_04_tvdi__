from ttkthemes import ThemedTk
from tkinter import ttk

class Window(ThemedTk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title('使用ttk的套件')
        style = ttk.Style(self)        
        topFrame = ttk.Frame(self,borderwidth=1,relief='groove')
        btn1 = ttk.Button(topFrame,text="按鈕1")
        btn1.pack(side='left')
        btn2 = ttk.Button(topFrame,text="按鈕2")
        btn2.pack(side='left')
        btn3 = ttk.Button(topFrame,text="按鈕3")
        btn3.pack(side='left')
        topFrame.pack(padx=10,pady=(10,0),expand=True,fill='x')
        bottomFrame = ttk.Frame(self,width=500,height=300,borderwidth=1,relief='groove')
        bottomFrame.pack(padx=10,pady=10)

def main():
    window = Window(theme="arc")
    window.mainloop()

if __name__ == '__main__':
    main()