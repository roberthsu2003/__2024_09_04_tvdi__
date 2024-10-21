from tkinter import ttk
import tkinter as tk
from ttkthemes import ThemedTk

class Window(ThemedTk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('登入')
        #==============style===============
        style = ttk.Style(self)
        style.configure('TopFrame.TLabel',font=('Helvetica',20))
        #============end style===============
        
        #==============top Frame===============

        topFrame = ttk.Frame(self)
        ttk.Label(topFrame,text='個人資訊輸入',style='TopFrame.TLabel').pack()
        topFrame.pack(padx=20,pady=20)
        
        #==============end topFrame===============

        #==============bottomFrame===============
        bottomFrame = ttk.Frame(self)
        bottomFrame.columnconfigure(index=0,weight=1)
        bottomFrame.columnconfigure(index=1,weight=9)
        ttk.Label(bottomFrame,text='UserName:').grid(column=0,row=0,padx=(10,0),sticky='E')

        self.username = tk.StringVar()
        ttk.Entry(bottomFrame,textvariable=self.username).grid(column=1,row=0,pady=10)
        
        ttk.Label(bottomFrame,text='Password:').grid(row=1,column=0,sticky='E')

        self.password = tk.StringVar()
        ttk.Entry(bottomFrame,textvariable=self.password).grid(column=1, row=1,pady=10,padx=10)
        
        

        cancel_btn = ttk.Button(bottomFrame,text='取消')
        cancel_btn.grid(column=0,row=2,padx=10,pady=(30,0))

        ok_btn = ttk.Button(bottomFrame,text='確定')
        ok_btn.grid(column=1, row=2,padx=10,pady=(30,0),sticky='E')
        bottomFrame.pack(expand=True,fill='x',padx=20,pady=(0,20),ipadx=10,ipady=10)
        #==============end bottomFrame===============
        

        


        



def main():
    window = Window(theme="arc")
    window.username.set('這裏放姓名')
    window.password.set('這裏打password')
    window.mainloop()

if __name__ == '__main__':
    main()