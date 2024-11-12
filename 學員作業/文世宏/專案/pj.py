from tkinter import ttk
import tkinter as tk
from ttkthemes import ThemedTk
from tkinter.messagebox import showinfo

class Window(ThemedTk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('登入')
        self.resizable(False, False)
        #==============style===============
        style = ttk.Style(self)
        style.configure('TopFrame.TLabel',font=('Helvetica',20))
        #============end style===============
        
        #==============top Frame===============

        topFrame = ttk.Frame(self)
        ttk.Label(topFrame,text='臺北市今日使用道路集會路段',style='TopFrame.TLabel').pack()
        topFrame.pack(padx=20,pady=20)
        
        #==============end topFrame===============
        
# 臺北市今日使用道路集會路段
# https://tpnco.blob.core.windows.net/blobfs/Rally/TodayRallyCase.json
# 臺北市今日臨時使用道路路段
# https://tpnco.blob.core.windows.net/blobfs/Rally/TodayUrgentCase.json
    
        
 

def main():
    window = Window(theme="arc")
    window.mainloop()

if __name__ == '__main__':
    main()