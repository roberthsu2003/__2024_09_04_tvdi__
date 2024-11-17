from ttkthemes import ThemedTk
from datasource import generate_orders, generate_sales_orders, save_to_csv, save_to_sqlite, load_from_sqlite
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
        print("Hello Tkinter and Python 1") 
        sales = datasource.get_sales()
        #self.selected_site = tk.StringVar()
        print("Hello Tkinter and Python 2") 
        self.selected_county = tk.StringVar()
        sitenames_cb = ttk.Combobox(self.selectedFrame, textvariable=self.selected_county,values=counties,state='readonly')
        self.selected_county.set('請選擇城市')
        sitenames_cb.bind('<<ComboboxSelected>>', self.county_selected)
        sitenames_cb.pack(anchor='n',pady=10)
        self.sitenameFrame = None 
        self.selectedFrame.pack(side='left',fill='y')
            #==============End SelectedFrame=============== 
            
        bottomFrame.pack()
        #==============end bottomFrame===============
    
    pass

    def county_selected(self,event):
        pass




def main():
   # Step 1: Generate orders
    orders = generate_orders()

    # Step 2: Generate sales orders data
    sales_data = generate_sales_orders(orders)

    # Step 3: Save sales data to CSV
    df = save_to_csv(sales_data)

    # Step 4: Save sales data to SQLite database
    save_to_sqlite(df)

    # Step 5: Load data back from SQLite database for verification
    loaded_df = load_from_sqlite()
    print("\nLoaded Data from SQLite:")
    print(loaded_df.head())
    
    sales = datasource.get_sales()
    
    window = Window(theme="arc")
    window.mainloop()



if __name__ == '__main__':
    main()