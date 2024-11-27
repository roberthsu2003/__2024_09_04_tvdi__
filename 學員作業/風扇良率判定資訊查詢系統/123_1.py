import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import pandas as pd


class Window(ThemedTk):
    def __init__(self, *args, **kwargs):
        super().__init__()
        # ======= 基本設置 =======
        self.title("風扇貼標正確判斷")
        # self.geometry("1200x400")  # 設定視窗大小
        style = ttk.Style(self)
        style.configure("Topframe.Tabel", font=("Helvetica", 20))  # 標題樣式
        font1 = ("標楷體", 16)

        # ======= 讀取數據 =======
        self.df = pd.read_csv('Factoryworkstation.csv')  # 調整為你的檔案路徑
        self.data = pd.read_csv('virtual_data_with_permissions.csv')
        self.frame0_data = pd.read_csv('orders_large.csv')

        # ======= 標題部分 =======
        topFrame = ttk.Frame(self)
        ttk.Label(topFrame, text="風扇貼標歪斜檢測", font=("Helvetica", 40)).pack(padx=20, pady=20)
        topFrame.pack()

        # ======= 中間選項部分 =======
        midFrame = ttk.Frame(self)
        #Date,Order ID,Product,Quantity
        # ======= frame0  =======
        frame0 = ttk.Frame(midFrame)
        # ======= frame0  =======
        # ================= date  =====================
        tk.Label(frame0, text="日期:", font=font1).pack(side="left", padx=5, pady=5)
        self.date_county = tk.StringVar()
        self.date_cobox = ttk.Combobox(
            frame0, textvariable=self.date_county,
            values=self.get_date_values('Date'),
            state="readonly",
            width=15
        )
        self.date_cobox.set("請選擇日期")
        self.date_cobox.pack(side="left", padx=5)
        self.date_cobox.bind("<<ComboboxSelected>>", self.update_OrderID_options)
        # ================= date  =====================
        # ================= OrderID  =====================
        tk.Label(frame0, text="訂單號碼:", font=font1).pack(side="left", padx=5, pady=5)
        self.OrderID_county = tk.StringVar()
        self.OrderID_cobox = ttk.Combobox(
            frame0, textvariable=self.OrderID_county,
            state="readonly",
            width=15
        )
        self.OrderID_cobox.set("訂單號碼:")
        self.OrderID_cobox.pack(side="left", padx=5)
        self.OrderID_cobox.bind("<<ComboboxSelected>>", self.update_Product_options)  # 這裡改為更新Product選項

        # ================= OrderID  =====================

        # ================= Product  =====================
        # ======= Product  =======
        tk.Label(frame0, text="訂單料號:", font=font1).pack(side="left", padx=5, pady=5)
        self.Product_county = tk.StringVar()
        self.Product_cobox = ttk.Combobox(
            frame0, textvariable=self.Product_county,
            state="readonly",
            width=15
        )
        self.Product_cobox.set("訂單料號")
        self.Product_cobox.pack(side="left", padx=5)
        # ================= Product  =====================

        # ================= Quantity  =====================
        tk.Label(frame0, text="訂單數量:", font=font1).pack(side="left", padx=5, pady=5)
        self.Quantity_county = tk.StringVar()
        self.Quantity_cobox = ttk.Combobox(
            frame0, textvariable=self.Quantity_county,
            # values=0,
            state="readonly",
            width=6
        )
        self.Quantity_cobox.set("訂單數量")
        self.Quantity_cobox.pack(side="left", padx=5)
        self.Quantity_cobox.bind("<<ComboboxSelected>>", self.update_workshop_options)
        # ================= Quantity  =====================
        frame0.pack()
        # ================= frame0  =====================
        # 第一排 (廠區、車間、工站)
        frame1 = ttk.Frame(midFrame)
        tk.Label(frame1, text="廠區:", font=font1).pack(side="left", padx=5, pady=5)
        self.Factory_county = tk.StringVar()
        self.Factory_cobox = ttk.Combobox(
            frame1, textvariable=self.Factory_county,
            values=self.get_unique_values('Plant'),
            state="readonly",
            width=10
        )
        self.Factory_cobox.set("請選擇廠區")
        self.Factory_cobox.pack(side="left", padx=5)
        self.Factory_cobox.bind("<<ComboboxSelected>>", self.update_workshop_options)

        tk.Label(frame1, text="車間:", font=font1).pack(side="left", padx=5, pady=5)
        self.workshop_county = tk.StringVar()
        self.workshop_cobox = ttk.Combobox(
            frame1, textvariable=self.workshop_county,
            state="readonly",
            width=10
        )
        self.workshop_cobox.set("請選擇車間")
        self.workshop_cobox.pack(side="left", padx=5)
        self.workshop_cobox.bind("<<ComboboxSelected>>", self.update_code_options)

        tk.Label(frame1, text="工站:", font=font1).pack(side="left", padx=5, pady=5)
        self.workstation_county = tk.StringVar()
        self.workstation_cobox = ttk.Combobox(
            frame1, textvariable=self.workstation_county,
            state="readonly",
            width=10
        )
        self.workstation_cobox.set("請選擇工站")
        self.workstation_cobox.pack(side="left", padx=5)

        frame1.pack(pady=10)

        # 第二排 (製造ID、品保ID、組長ID)
        frame2 = ttk.Frame(midFrame)
        tk.Label(frame2, text="製造者ID:", font=font1).pack(side="left", padx=5, pady=5)
        self.manufacturer_id = tk.StringVar()
        self.manufacturer_cobox = ttk.Combobox(
            frame2, textvariable=self.manufacturer_id,
            state="readonly",
            width=15
        )
        
        self.manufacturer_cobox.set("請選擇製造者ID")
        self.manufacturer_cobox.pack(side="left", padx=5)
        self.manufacturer_cobox.bind("<<ComboboxSelected>>", self.update_manufacturer_options)
        frame3 = ttk.Frame(midFrame)
        tk.Label(frame3, text="製造者:", font=font1).pack(side="left", padx=5, pady=5)
        tk.Label(frame3, text="製造者", font=font1,bg='white', fg='black',relief='solid',bd=1).pack(side="left", padx=5, pady=5)
        #============================製造者=====================================================
        tk.Label(frame2, text="品保ID:", font=font1).pack(side="left", padx=5, pady=5)
        self.qa_id = tk.StringVar()
        self.qa_cobox = ttk.Combobox(
            frame2, textvariable=self.qa_id,
            state="readonly",
            width=15
        )
        self.qa_cobox.set("請選擇品保ID")
        self.qa_cobox.pack(side="left", padx=5)

        tk.Label(frame3, text="品保:", font=font1).pack(side="left", padx=5, pady=5)
        tk.Label(frame3, text="品保", font=font1,bg='white', fg='black',relief='solid',bd=1).pack(side="left", padx=5, pady=5)

        tk.Label(frame2, text="組長ID:", font=font1).pack(side="left", padx=5, pady=5)
        self.supervisor_id = tk.StringVar()
        self.supervisor_cobox = ttk.Combobox(
            frame2, textvariable=self.supervisor_id,
            state="readonly",
            width=15
        )

        self.supervisor_cobox.set("請選擇組長ID")
        self.supervisor_cobox.pack(side="left", padx=5)
        tk.Label(frame3, text="組長:", font=font1).pack(side="left", padx=5, pady=5)
        tk.Label(frame3, text="組長", font=font1,bg='white', fg='black',relief='solid',bd=1).pack(side="left", padx=5, pady=5)
        frame2.pack(pady=10)
        frame3.pack(pady=10)
        midFrame.pack(pady=20)

    # ======= 工具方法 =======
    def get_date_values(self,name):
        return self.frame0_data[name].dropna().unique().tolist()
    
    def update_OrderID_options(self, event):
        selected_date = self.date_county.get()
        if selected_date:
            filtered_OrderID = self.frame0_data[self.frame0_data['Date'] == selected_date]['OrderID'].unique().tolist()
            self.OrderID_cobox['values'] = filtered_OrderID
            
    def update_Product_options(self, event):
        selected_date = self.date_county.get()  # 取得選擇的日期
        selected_order_id = self.OrderID_county.get() 
        self.OrderID_cobox.set("訂單號碼") # 取得選擇的訂單號碼
        
        if selected_date and selected_order_id:
            # 根據 Date 和 OrderID 篩選符合條件的 Product
            filtered_products = self.frame0_data[(
                self.frame0_data['Date'] == selected_date) &  # 篩選符合選擇的日期
                (self.frame0_data['OrderID'] == selected_order_id)]  # 篩選符合選擇的訂單號碼
            filtered_products = filtered_products['Product'].unique().tolist()
            self.Product_cobox['values'] = filtered_products  # 更新產品選項
            self.Product_cobox.set("訂單料號")  # 重置 Product 選項

    def get_unique_values(self, column_name):
        """
        獲取指定欄位的唯一值列表
        """
        return self.df[column_name].dropna().unique().tolist()

    # ======= 更新事件 =======
    def update_workshop_options(self, event):
        """
        根據選擇的廠區更新車間選項
        """
        selected_plant = self.Factory_county.get()
        if selected_plant:
            filtered_workstations = self.df[self.df['Plant'] == selected_plant]['Workstation Code'].unique().tolist()
            self.workshop_cobox['values'] = filtered_workstations
            self.workshop_cobox.set("請選擇車間")  # 重置車間選項
            self.workstation_cobox.set("請選擇工站")  # 重置工站選項
            self.workstation_cobox['values'] = []  # 清空工站選單

    def update_code_options(self, event):
        """
        根據選擇的車間更新工站選項
        """
        selected_plant = self.Factory_county.get()
        selected_workstation = self.workshop_county.get()
        if selected_plant and selected_workstation:
            filtered_codes = self.df[(self.df['Plant'] == selected_plant) & 
                                     (self.df['Workstation Code'] == selected_workstation)]['Code'].unique().tolist()
            self.workstation_cobox['values'] = filtered_codes
            self.workstation_cobox.set("請選擇工站")  # 重置工站選項

    def update_manufacturer_options(self,event):
        selcted_manufacturer = self.manufacturer.get()
        # return self.d[column_name].dropna().unique().tolist()
    def data_updata(self,event):
        workstation_city = event.widget.get()

if __name__ == "__main__":
    window = Window()
    window.mainloop()
