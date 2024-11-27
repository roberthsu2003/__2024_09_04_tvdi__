import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import pandas as pd

class Window(ThemedTk):
    def __init__(self, *args, **kwargs):
        super().__init__()
        # ======= 基本設置 =======
        self.title("風扇貼標正確判斷")
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
        frame0 = ttk.Frame(midFrame)

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
        self.OrderID_cobox.set("訂單號碼")
        self.OrderID_cobox.pack(side="left", padx=5)
        self.OrderID_cobox.bind("<<ComboboxSelected>>", self.update_Product_Quantity)  # 更新Product和Quantity選項

        # ================= OrderID  =====================

        # ================= Product  =====================
        tk.Label(frame0, text="訂單料號:", font=font1).pack(side="left", padx=5, pady=5)
        self.Product_county = tk.StringVar()
        self.Product_cobox = ttk.Combobox(
            frame0, textvariable=self.Product_county,
            state="readonly",
            width=15
        )
        self.Product_cobox.set("訂單料號")
        self.Product_cobox.pack(side="left", padx=5)

        # ================= Quantity  =====================
        tk.Label(frame0, text="訂單數量:", font=font1).pack(side="left", padx=5, pady=5)
        self.Quantity_county = tk.StringVar()
        self.Quantity_cobox = ttk.Combobox(
            frame0, textvariable=self.Quantity_county,
            state="readonly",
            width=6
        )
        self.Quantity_cobox.set("訂單數量")
        self.Quantity_cobox.pack(side="left", padx=5)
        frame0.pack()

        # ================= frame1  =====================
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

        # 品保ID (代號 2)
        tk.Label(frame2, text="品保ID:", font=font1).pack(side="left", padx=5, pady=5)
        self.quality_control_id = tk.StringVar()
        self.quality_control_cobox = ttk.Combobox(
            frame2, textvariable=self.quality_control_id,
            state="readonly",
            width=15
        )
        
        self.quality_control_cobox.set("請選擇品保ID")
        self.quality_control_cobox.pack(side="left", padx=5)

        # 組長ID (代號 3)
        tk.Label(frame2, text="組長ID:", font=font1).pack(side="left", padx=5, pady=5)
        self.team_leader_id = tk.StringVar()
        self.team_leader_cobox = ttk.Combobox(
            frame2, textvariable=self.team_leader_id,
            state="readonly",
            width=15
        )
        self.team_leader_cobox.set("請選擇組長ID")
        self.team_leader_cobox.pack(side="left", padx=5)

        # 更新製造者ID、品保ID、組長ID選項
        self.update_manufacturer_options()  # 初始更新製造者ID選項
        self.update_quality_control_options()  # 初始更新品保ID選項
        self.update_team_leader_options()  # 初始更新組長ID選項

        frame2.pack(pady=10)
        frame3 = ttk.Frame(midFrame)
        tk.Label(frame3, text="製造者:", font=font1).pack(side="left", padx=5, pady=5)
        self.manufacturer_id = tk.StringVar()
        self.manufacturer_cobox = ttk.Combobox(
            frame3, textvariable=self.manufacturer_id,
            state="readonly",
            width=15
        )
        self.manufacturer_cobox.set("請選擇製造者")
        self.manufacturer_cobox.pack(side="left", padx=5)

        # 品保ID (代號 2)
        tk.Label(frame3, text="品保:", font=font1).pack(side="left", padx=5, pady=5)
        self.quality_control_id = tk.StringVar()
        self.quality_control_cobox = ttk.Combobox(
            frame3, textvariable=self.quality_control_id,
            state="readonly",
            width=15
        )
        self.quality_control_cobox.set("請選擇品保")
        self.quality_control_cobox.pack(side="left", padx=5)

        # 組長ID (代號 3)
        tk.Label(frame3, text="組長:", font=font1).pack(side="left", padx=5, pady=5)
        self.team_leader_id = tk.StringVar()
        self.team_leader_cobox = ttk.Combobox(
            frame3, textvariable=self.team_leader_id,
            state="readonly",
            width=15
        )
        self.team_leader_cobox.set("請選擇組長")
        self.team_leader_cobox.pack(side="left", padx=5)


        frame3.pack(pady=10)
        midFrame.pack(pady=20)

    # ======= 工具方法 =======
    def get_date_values(self, name):
        return self.frame0_data[name].dropna().unique().tolist()

    def update_OrderID_options(self, event):
        selected_date = self.date_county.get()
        if selected_date:
            filtered_OrderID = self.frame0_data[self.frame0_data['Date'] == selected_date]['OrderID'].unique().tolist()
            self.OrderID_cobox['values'] = filtered_OrderID

    def update_Product_Quantity(self, event):
        selected_date = self.date_county.get()  # 取得選擇的日期
        selected_order_id = self.OrderID_county.get()  # 取得選擇的訂單號碼
        
        if selected_date and selected_order_id:
            # 根據 Date 和 OrderID 篩選符合條件的 Product 和 Quantity
            filtered_data = self.frame0_data[
                (self.frame0_data['Date'] == selected_date) & 
                (self.frame0_data['OrderID'] == selected_order_id)
            ]
            
            # 更新訂單料號 (Product) 和 訂單數量 (Quantity) 選項
            products = filtered_data['Product'].unique().tolist()
            quantities = filtered_data['Quantity'].unique().tolist()

            self.Product_cobox['values'] = products
            self.Quantity_cobox['values'] = quantities

            if products:
                self.Product_cobox.set(products[0])  # 預設選擇第一個產品料號
            if quantities:
                self.Quantity_cobox.set(quantities[0])  # 預設選擇第一個訂單數量

    def get_unique_values(self, column_name):
        return self.df[column_name].dropna().unique().tolist()

    def update_workshop_options(self, event):
        selected_plant = self.Factory_county.get()
        if selected_plant:
            filtered_workstations = self.df[self.df['Plant'] == selected_plant]['Workstation Code'].unique().tolist()
            self.workshop_cobox['values'] = filtered_workstations
            self.workshop_cobox.set("請選擇車間")
            self.workstation_cobox.set("請選擇工站")
            self.workstation_cobox['values'] = []

    def update_code_options(self, event):
        selected_plant = self.Factory_county.get()
        selected_workstation = self.workshop_county.get()
        if selected_plant and selected_workstation:
            filtered_codes = self.df[
                (self.df['Plant'] == selected_plant) & 
                (self.df['Workstation Code'] == selected_workstation)
            ]['Code'].unique().tolist()
            self.workstation_cobox['values'] = filtered_codes
            self.workstation_cobox.set("請選擇工站")
    def update_manufacturer_options(self):
        # 只顯示權限代號為1的ID
        manufacturer_ids = self.data[self.data['權限代號'] == 1]['ID'].unique().tolist()
        self.manufacturer_cobox['values'] = manufacturer_ids
        if manufacturer_ids:
            self.manufacturer_cobox.set(manufacturer_ids[0])  # 預設選擇第一個製造者ID

    def update_quality_control_options(self):
        # 只顯示權限代號為2的ID (品保)
        quality_control_ids = self.data[self.data['權限代號'] == 2]['ID'].unique().tolist()
        self.quality_control_cobox['values'] = quality_control_ids
        if quality_control_ids:
            self.quality_control_cobox.set(quality_control_ids[0])  # 預設選擇第一個品保ID

    def update_team_leader_options(self):
        # 只顯示權限代號為3的ID (組長)
        team_leader_ids = self.data[self.data['權限代號'] == 3]['ID'].unique().tolist()
        self.team_leader_cobox['values'] = team_leader_ids
        if team_leader_ids:
            self.team_leader_cobox.set(team_leader_ids[0])  # 預設選擇第一個組長ID

if __name__ == "__main__":
    window = Window()
    window.mainloop()
