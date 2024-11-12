import tkinter as tk
import tkinter as tk
from tkinter import ttk

class Window(tk.Tk):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.title("我的專題")
        self.geometry('500x300')
        message=ttk.Label(self,text="專題名稱")
        message.pack()

def main():
    window=Window()
    window.mainloop()


if __name__ == '__main__':
    main()