from ttkthemes import ThemedTk
import datasource
import tkinter as tk
from tkinter import ttk
import view
import simulate_input


class Window(ThemedTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Cooling Fan Indicators')
        self.resizable(False, False)
        # ============== Style ===============
        style = ttk.Style(self)
        style.configure('TopFrame.TLabel', font=('標楷體', 20))
        # =========== Top Frame =============
        topFrame = ttk.Frame(self)
        ttk.Label(topFrame, text='冷卻風扇生產指標', style='TopFrame.TLabel').pack()
        topFrame.pack(padx=20, pady=20)
        # =========== Bottom Frame ==========
        bottomFrame = ttk.Frame(self, padding=[10, 10, 10, 10])
        # =========== Selected Frame ==========
        self.selectedFrame = ttk.Frame(self, padding=[10, 10, 10, 10])
        # Refresh button
        icon_button = view.ImageButton(self.selectedFrame, command=lambda: datasource.load_from_sqlite())
        icon_button.pack()
        # Combobox to select sales
        sales_list = datasource.get_sales()
        print("Returned Sales List:", sales_list)  # Debugging
        self.sales_selected = tk.StringVar()  
        # self.sales_selected Is a StringVar which can't be called by event handler with the same name
        customer_cb = ttk.Combobox(
            self.selectedFrame, textvariable=self.sales_selected, values=sales_list, state='readonly'
        )
        self.sales_selected.set('請選擇業務名稱')

        # Correctly bind the event handler
        customer_cb.bind('<<ComboboxSelected>>', self.on_sales_selected)

        customer_cb.pack(anchor='n', pady=10)
        self.customerFrame = None
        self.selectedFrame.pack(side='left', fill='y')
        # =========== Right Frame ==========
        rightFrame = ttk.LabelFrame(bottomFrame, text="產品生產指標", padding=[10, 10, 10, 10])
        # TreeView columns
        columns = (
            'Sales ID', 'Sales Name', 'Customer ID', 'Order ID', 'Yield Rate',
            'Thru_put', 'Order Date', 'Delivery Date', 'Factory'
        )
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
            #==============End RightFRame==================      
        
        
        
        bottomFrame.pack()
        #==============end bottomFrame===============

    def on_sales_selected(self, event):
        selected_sales = self.sales_selected.get()
        print(f"Selected Sales Name: {selected_sales}")  # Debugging
        customers = datasource.get_customer_id(selected_sales)
        print(f"Hello Tkinter and Python 1: {customers}")  # Debugging
       
        pass


def main():
    window = Window(theme="arc")
    window.mainloop()


if __name__ == '__main__':
    # Generate the simulated data
    csv_file = 'sales_orders.csv'
    db_file = 'sales_orders.db'
    table_name = 'sales_orders'

    # Call the function from the package
    data_frame = simulate_input.generate_sales_data(csv_filename=csv_file, db_filename=db_file, table_name=table_name)

    # Display the first few rows of the data
    print(data_frame.head())
    
    main()
