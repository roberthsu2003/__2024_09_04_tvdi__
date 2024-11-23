from ttkthemes import ThemedTk
import datasource
import tkinter as tk
from tkinter import ttk
import view


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
        # customers = datasource.get_customers_by_sales_id(selected_sales)
        customers = datasource.get_customerid(selected_sales)
        print(f"Hello Tkinter and Python 1: {customers}")  # Debugging
        # if self.customerFrame:
        #     self.customerFrame.destroy()
        self.customerFrame = view.CustomerFrame(master=self.selectedFrame, customers=customers)
        
        self.bind("<<Radio_Button_Selected>>", self.radio_button_click)
        self.customerFrame.pack()
        
     def radio_button_click(self, event):
        selected_customer = event.widget.selected_customer
        for children in self.tree.get_children():
            self.tree.delete(children)
        selected_data = datasource.get_selected_data(selected_customer)
        for record in selected_data:
            self.tree.insert("", "end", values=record)
        dataframe = datasource.get_plot_data(customer_id=selected_customer)
        axes = dataframe.plot()
        figure = axes.get_figure()
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(figure, master=self.plotFrame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(20, 10))


def main():
    window = Window(theme="arc")
    window.mainloop()


if __name__ == '__main__':
    main()
