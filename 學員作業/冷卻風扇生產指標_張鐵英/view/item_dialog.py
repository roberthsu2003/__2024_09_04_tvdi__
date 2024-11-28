import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import Dialog
from PIL import Image, ImageTk
import tkintermapview as tkmap

class MyCustomDialog(Dialog):
    def __init__(self,parent,sales_orders:list,title=None):
        self.sales_id = sales_orders[0]
        self.sales_name = sales_orders[1]
        self.customer_id = sales_orders[2]
        self.order_id=sales_orders[3]
        self.yield_rate = sales_orders[4]
        self.thru_put = sales_orders[5]
        self.order_date = float(sales_orders[6])
        self.deliver_date = float(sales_orders[7])
        self.factory = sales_orders[8]
        super().__init__(parent=parent,title=title)

    

        