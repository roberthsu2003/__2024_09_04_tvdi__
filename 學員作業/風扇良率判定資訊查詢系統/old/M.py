import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter.messagebox import showinfo
import fan1 as f


class Window(ThemedTk):
    def __init__(self, *args, **kwargs):
        super().__init__()

        # ==================== Style =====================
        self.title('風扇貼標正確判斷')  # 顯示窗口標題
        # self.geometry("1024x800")  # 設定窗口大小

        style = ttk.Style(self)
        style.configure("Topframe.Tabel", font=('Helvetica', 20))  # 標題字型
        font1 = ('標楷體', 18)

        # ==================== TOP frame =====================
        topFrame = ttk.Frame(self)  # 創建一個框架
        ttk.Label(topFrame, text='風扇貼標歪斜檢測', font=('Helvetica', 40)).pack(padx=50, pady=50)
        topFrame.pack()

        # ==================== Mid frame =====================
        midFrame = ttk.Frame(self)

        # 廠區選擇
        self.Factory_county = tk.StringVar()
        Factory_LB = tk.Label(midFrame, text="製造ID:", font=font1)
        Factory_LB.grid(row=0, column=0, padx=10, pady=10)
        Factory_cobox = ttk.Combobox(
            midFrame, textvariable=self.Factory_county, values=f.plant_list, state="readonly", width=10
        )
        Factory_cobox.set("請選擇廠區")
        Factory_cobox.grid(row=0, column=1, padx=10, pady=10)
        Factory_cobox.bind("<<ComboboxSelected>>", self.Factory_county)

        # 車間選擇
        self.workshop_county = tk.StringVar()
        workshop_LB = tk.Label(midFrame, text="車間:", font=font1)
        workshop_LB.grid(row=0, column=2, padx=10, pady=10)
        workshop_cobox = ttk.Combobox(
            midFrame, textvariable=self.workshop_county, values=f.WorkstationCode_list, state="readonly", width=10
        )
        workshop_cobox.set("請選擇車間")
        workshop_cobox.grid(row=0, column=3, padx=10, pady=10)
        workshop_cobox.bind("<<ComboboxSelected>>", self.workshop_county)

        # 工站選擇
        self.workstation_county = tk.StringVar()
        workstation_LB = tk.Label(midFrame, text="工站:", font=font1)
        workstation_LB.grid(row=0, column=4, padx=10, pady=10)
        workstation_cobox = ttk.Combobox(
            midFrame, textvariable=self.workstation_county, values=f.Code_list, state="readonly", width=10
        )
        workstation_cobox.set("請選擇工站")
        workstation_cobox.grid(row=0, column=5, padx=10, pady=10)
        workstation_cobox.bind("<<ComboboxSelected>>", self.workstation)

        midFrame.pack()

        # ==================== Canvas =====================
        canvas = tk.Canvas(self, width=350, height=250)
        canvas.pack()

        for index, (role, data_dict) in enumerate(f.roles.items()):
            self.create_role_selector(canvas, 30 + index * 70, role, data_dict)
    def create_role_selector(self, canvas, y, role, data_dict):
        # 根據角色和數據字典創建選擇框
        id_var = tk.StringVar()
        name_var = tk.StringVar()

        canvas.create_text(50, y, text=f"{role}ID:", anchor='w')
        id_menu = ttk.Combobox(self, textvariable=id_var, values=list(data_dict.keys()))
        canvas.create_window(150, y, window=id_menu, anchor='w')
        id_menu.bind("<<ComboboxSelected>>", lambda _: name_var.set(data_dict.get(id_var.get(), "")))

        canvas.create_text(50, y + 30, text=f"{role}:", anchor='w')
        name_label = tk.Label(self, textvariable=name_var)
        canvas.create_window(150, y + 30, window=name_label, anchor='w')

    def Factory_county(self, event):
        # 廠區選擇後的處理
        Factory_city = event.widget.get()
        print(f"選擇的廠區是: {Factory_city}")

    def workshop_county(self, event):
        # 車間選擇後的處理
        workshop_city = event.widget.get()
        print(f"選擇的車間是: {workshop_city}")

    def workstation(self, event):
        # 工站選擇後的處理
        workstation_city = event.widget.get()
        print(f"選擇的工站是: {workstation_city}")



if __name__ == "__main__":
    window = Window()
    window.mainloop()
