from ttkthemes import ThemedTk
import datasource
import tkinter as tk
from tkinter import ttk
import view



class Window(ThemedTk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Cooling Fan Indicators')
        self.resizable(False, False)
        #==============style===============
        style = ttk.Style(self)
        style.configure('TopFrame.TLabel',font=('標楷體',20))
        #============end style===============
        #==============top Frame===============
        topFrame = ttk.Frame(self)
        ttk.Label(topFrame,text='冷卻風扇生產指標',style='TopFrame.TLabel').pack()
        topFrame.pack(padx=20,pady=20)
        #==============end topFrame===============
        
        #==============bottomFrame===============
        bottomFrame = ttk.Frame(self,padding=[10,10,10,10])
            #==============SelectedFrame===============        
        self.selectedFrame= ttk.Frame(self,padding=[10,10,10,10])
        #增加refresh button        
        icon_button = view.ImageButton(self.selectedFrame,
                                       command=lambda:datasource.load_from_sqlite())
        icon_button.pack()
        #combobox選擇城市     
        
        sales_list = datasource.get_sales()
        #self.selected_site = tk.StringVar()
        print("Hello Tkinter and Python 2") 
        
        self.selected_sales = tk.StringVar()
        sitenames_cb = ttk.Combobox(self.selectedFrame, textvariable=self.selected_sales,values=sales_list,state='readonly')
        self.selected_sales.set('請選擇業務')
        sitenames_cb.bind('<<ComboboxSelected>>', self.selected_sales)
        sitenames_cb.pack(anchor='n',pady=10)
        self.sitenameFrame = None 
        self.selectedFrame.pack(side='left',fill='y')
        print("Hello Tkinter and Python 1") 
            #==============End SelectedFrame=============== 
            
        bottomFrame.pack()
        #==============end bottomFrame===============
    
    pass

    def selected_sales(self,event):
        pass




def main():
    window = Window(theme="arc")
    window.mainloop()



if __name__ == '__main__':
    main()