from ttkthemes import ThemedTk
from tkinter import ttk

class Window(ThemedTk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title('使用ttk的套件')
        style = ttk.Style(self)

        style.configure('Main.TButton',font=("Arial",15,"bold"),foreground="black")
        style.configure('Main1.TButton',font=("Arial",15,"bold"),background="lightblue",foreground="sky blue")
        style.configure('Main2.TButton',font=("Arial",15,"italic"),foreground="red")
        style.configure('Main3.TButton',font=("Arial",15,"underline"),foreground="violet")
        style.configure('Main4.TButton',font=("Arial",15,"overstrike"),foreground="black")
        #================================start topframe====================================
        topFrame = ttk.Frame(self,borderwidth=1,relief='groove')
        btn1 = ttk.Button(topFrame,text="加入購物車",style='Main.TButton',command=self.user_click1)
        btn1.pack(side='left',expand=True,fill='both',padx=10)
        btn2 = ttk.Button(topFrame,text="我的最愛",style='Main.TButton',command=self.user_click2)
        btn2.pack(side='left',expand=True,fill='both')
        btn3 = ttk.Button(topFrame,text="個人資料",style='Main.TButton',command=self.user_click3)
        btn3.pack(side='left',expand=True,fill='both',padx=10)
        topFrame.pack(padx=10,pady=(10,0),ipadx=10,ipady=10,expand=True,fill='both')
        #================================end topframe=====================================

        #================================start bottomframe================================
        bottomFrame = ttk.Frame(self,height=300,borderwidth=1,relief='groove')
      
        #================================start leftframe================================
        leftFrame =ttk.Frame(bottomFrame,width=100,height=300,borderwidth=2,relief='groove')
        btn1 = ttk.Button(leftFrame,text="Home",style='Main1.TButton')
        btn1.pack(expand=True,fill='x',padx=10,pady=5,ipady=50)
        btn2 = ttk.Button(leftFrame,text="Cancel",style='Main2.TButton')
        btn2.pack(expand=True,fill='x',padx=10,pady=5,ipady=25)
        btn3 = ttk.Button(leftFrame,text="Chat",style='Main1.TButton')
        btn3.pack(expand=True,fill='x',padx=10,pady=5,ipady=25)
        leftFrame.pack(padx=10,pady=10,side="left",expand=True,fill='both')
        #================================end leftframe================================

        #================================start centerframe================================
        centerFrame =ttk.Frame(bottomFrame,width=100,height=300,borderwidth=2,relief='groove')
        btn1 = ttk.Button(centerFrame,text="已刪除",style='Main4.TButton')
        btn1.pack(expand=True,fill='x',padx=10,pady=5,ipady=40)
        btn2 = ttk.Button(centerFrame,text="按鈕2")
        btn2.pack(expand=True,fill='x',padx=10,pady=5,ipady=20)
        btn3 = ttk.Button(centerFrame,text="已消失",style='Main4.TButton')
        btn3.pack(expand=True,fill='x',padx=10,pady=5,ipady=40)
        centerFrame.pack(padx=10,pady=10,side="left",expand=True,fill='both')
        #================================end centerframe=============================

        #================================start rightframe==============================
        rightFrame =ttk.Frame(bottomFrame,width=100,height=300,borderwidth=2,relief='groove')
        btn1 = ttk.Button(rightFrame,text="按鈕1",style='Main3.TButton')
        btn1.pack(expand=True,fill='x',padx=10,pady=5,ipady=33)
        btn2 = ttk.Button(rightFrame,text="按鈕2",style='Main3.TButton')
        btn2.pack(expand=True,fill='x',padx=10,pady=5,ipady=33)
        btn3 = ttk.Button(rightFrame,text="按鈕3",style='Main3.TButton')
        btn3.pack(expand=True,fill='x',padx=10,pady=5,ipady=34)
        rightFrame.pack(padx=10,pady=10,side="right",expand=True,fill='both')
        #================================end rightframe=================================
        bottomFrame.pack(padx=10,pady=10,expand=True,fill='both')
        #================================end bottomframe==================================

    def user_click1(self):
        print("Hello!button1")

    def user_click2(self):
        print("Hello!button2")

    def user_click3(self):
        print("Hello1 button3")

def main():
    window = Window(theme="arc")
    window.mainloop()

if __name__ == '__main__':    
    main()