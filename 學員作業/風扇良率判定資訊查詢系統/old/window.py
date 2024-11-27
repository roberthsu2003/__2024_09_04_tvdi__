import tkinter as tk
from tkinter import ttk
import pandas as pd

# 讀取CSV檔案
data = pd.read_csv('virtual_data_with_permissions.csv')

# 根據權限代號過濾各角色
roles = {
    "製造者": data[data['權限代號'] == 1].set_index('ID')['姓名'].to_dict(),
    "組長": data[data['權限代號'] == 2].set_index('ID')['姓名'].to_dict(),
    "品保員": data[data['權限代號'] == 3].set_index('ID')['姓名'].to_dict(),
}

# 建立視窗
window = tk.Tk()
window.title("人員選取")
window.geometry("350x250")
window.resizable(False, False)

# 設置 Canvas
canvas = tk.Canvas(window, width=350, height=250)
canvas.pack()

# 創建選單並更新名稱的函數
def create_role_selector(canvas, y, role, data_dict):
    id_var = tk.StringVar()
    name_var = tk.StringVar()

    canvas.create_text(50, y, text=f"{role}ID:", anchor='w')
    id_menu = ttk.Combobox(window, textvariable=id_var, values=list(data_dict.keys()))
    canvas.create_window(150, y, window=id_menu, anchor='w')
    id_menu.bind("<<ComboboxSelected>>", lambda _: name_var.set(data_dict.get(id_var.get(), "")))

    canvas.create_text(50, y + 30, text=f"{role}:", anchor='w')
    name_label = tk.Label(window, textvariable=name_var)
    canvas.create_window(150, y + 30, window=name_label, anchor='w')

# 迭代創建所有角色選單
for index, (role, data_dict) in enumerate(roles.items()):
    create_role_selector(canvas, 30 + index * 70, role, data_dict)

# 開啟視窗
window.mainloop()
