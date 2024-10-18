from ttkthemes import ThemedTk
from tkinter import ttk

class Window(ThemedTk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title('使用ttk的套件')
        style = ttk.Style(self)        
        topFrame = ttk.Frame(self,width=300,height=100,borderwidth=1,relief='groove')
        topFrame.pack(pady=(10,0))
        bottomFrame = ttk.Frame(self,width=500,height=300,borderwidth=1,relief='groove')
        bottomFrame.pack(padx=10,pady=10)

def main():
    window = Window(theme="arc")
    window.mainloop()

if __name__ == '__main__':
    main()