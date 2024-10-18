import tkinter as tk
from tkinter import ttk

class Window(tk.Tk):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.title('使用ttk的套件')
        self.geometry('400x300')
        style = ttk.Style(self)
        style.configure('TLabel',font=('Helvetica', 11)) #修改現有的
        style.configure('Title.TLabel',font=('Helvetica', 15)) #自訂的style

        message = ttk.Label(self,text='使用ttk的Label',style='Title.TLabel')
        print(message.winfo_class())
        message.pack()

def main():
    window = Window()
    window.mainloop()

if __name__ == '__main__':
    main()