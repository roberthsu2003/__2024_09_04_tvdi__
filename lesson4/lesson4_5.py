from ttkthemes import ThemedTk
from tkinter import ttk

class Window(ThemedTk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title('使用ttk的套件')
        self.geometry('400x300')
        style = ttk.Style(self)        
        style.configure('Main.TButton',font=('Arial',15))
        btn1 = ttk.Button(self,text="Button Demo",style='Main.TButton')
        btn1.pack(ipadx=10,ipady=10,padx=10,pady=10)

def main():
    window = Window(theme="arc")
    window.mainloop()

if __name__ == '__main__':
    main()