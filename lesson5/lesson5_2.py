from tkinter import ttk
import tkinter as tk
from ttkthemes import ThemedTk
from tkinter.messagebox import showinfo

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
        ttk.Label(topFrame,text='請多選一',style='TopFrame.TLabel').pack()
        topFrame.pack(padx=20,pady=20)
        
        #==============end topFrame===============

        #==============bottomFrame===============
        bottomFrame = ttk.Frame(self)
        self.selected_size = tk.StringVar()
        sizes = (('Small', 'S'),
                ('Medium', 'M'),
                ('Large', 'L'),
                ('Extra Large', 'XL'),
                ('Extra Extra Large', 'XXL'))
        
        label = ttk.Label(bottomFrame,text="What's your t-shirt size?")
        label.pack(fill='x', padx=5, pady=5)

        for size in sizes:
            r = ttk.Radiobutton(
                bottomFrame,
                text=size[0],
                value=size[1],
                variable=self.selected_size
            )
            r.pack(fill='x', padx=5, pady=5)

        # button
        button = ttk.Button(
            bottomFrame,
            text="Get Selected Size",
            command=self.show_selected_size)

        button.pack(fill='x', padx=5, pady=5)

        bottomFrame.pack(expand=True,fill='x',padx=20,pady=(0,20),ipadx=10,ipady=10)
        #==============end bottomFrame===============

    def show_selected_size(self):
        showinfo(
            title='Result',
            message=self.selected_size.get()
        )
    
        

def main():
    window = Window(theme="arc")
    #window.username.set('這裏放姓名')
    #window.password.set('這裏打password')
    window.mainloop()

if __name__ == '__main__':
    main()