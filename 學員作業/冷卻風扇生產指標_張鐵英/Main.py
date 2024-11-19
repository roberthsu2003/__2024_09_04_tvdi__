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
        self.selected_sales = tk.StringVar()
        customer_cb = ttk.Combobox(self.selectedFrame, textvariable=self.selected_sales,values=sales_list,state='readonly')
        self.selected_sales.set('請選擇業務名稱')
        customer_cb.bind('<<ComboboxSelected>>', self.selected_sales)
        customer_cb.pack(anchor='n',pady=10)
        self.customerFrame = None 
        self.selectedFrame.pack(side='left',fill='y')
            #==============End SelectedFrame=============== 
            
            #==============RightFrame======================
        rightFrame = ttk.LabelFrame(bottomFrame,text="產品生產指標",padding=[10,10,10,10])
        #建立treeView
        # define columns
        print("Hello Tkinter and Python 2") 
        columns = ('Sales ID', 'Sales Name', 'Customer ID','Order ID', 'Yield Rate','Thru_put','Order Date','Delivery Date','Factory')
        self.tree = ttk.Treeview(rightFrame, columns=columns, show='headings')
        # self.tree.bind('<<TreeviewSelect>>', self.item_selected)
        # define headings
        self.tree.heading('Sales ID', text='業務代號')
        self.tree.heading('Sales Name', text='業務名稱')
        self.tree.heading('Customer ID', text='客戶代號')
        self.tree.heading('Order ID', text='訂單號碼')
        self.tree.heading('Yield Rate', text='良率')
        self.tree.heading('Thru_put',text='直通率')
        self.tree.heading('Order Date', text='下單日期')
        self.tree.heading('Delivery Date', text='交貨日期')
        self.tree.heading('Factory', text='生產工廠')
        self.tree.column('Sales ID', width=80,anchor="center")
        self.tree.column('Sales Name', width=100,anchor="center")
        self.tree.column('Customer ID', width=120,anchor="center")
        self.tree.column('Order ID', width=80,anchor="center")
        self.tree.column('Yield Rate', width=50,anchor="center")
        self.tree.column('Thru_put', width=50,anchor="center")
        self.tree.column('Order Date', width=100,anchor="center")
        self.tree.column('Delivery Date', width=100,anchor="center")
        self.tree.column('Factory', width=80, anchor="center")
        self.tree.pack(side='right')
        rightFrame.pack(side='right')
        print("Hello Tkinter and Python 1") 
            #==============End RightFRame==================      
            
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