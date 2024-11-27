import tkinter as tk
from tkinter import ttk
import pandas as pd
import csv

df = pd.read_csv('Factoryworkstation.csv')

plant_list = df['Plant'].dropna().unique().tolist()
WorkstationCode_list = (df[df['Plant'].isin(plant_list)]['Workstation Code'].dropna().unique().tolist())
Code_list = (df[df['Workstation Code'].isin(WorkstationCode_list)]['Code'].dropna().unique().tolist())


    # 讀取CSV檔案
data = pd.read_csv('virtual_data_with_permissions.csv')

    # 根據權限代號過濾各角色
roles = {
        "製造者": data[data['權限代號'] == 1].set_index('ID')['姓名'].to_dict(),
        "組長": data[data['權限代號'] == 2].set_index('ID')['姓名'].to_dict(),
        "品保員": data[data['權限代號'] == 3].set_index('ID')['姓名'].to_dict(),
    }
# 假設你要查找某個特定 ID 的姓名
id_to_find = 123

# 查找該 ID 所對應的姓名
import pandas as pd

# 假設這是你的資料框（data）

# 根據權限代號 1 (製造者) 抓取姓名
製造者_姓名 = data[data['權限代號'] == 1]['姓名'].tolist()
print("製造者姓名:", 製造者_姓名)

# 根據權限代號 2 (組長) 抓取姓名
組長_姓名 = data[data['權限代號'] == 2]['姓名'].tolist()
print("組長姓名:", 組長_姓名)

# 根據權限代號 3 (品保員) 抓取姓名
品保員_姓名 = data[data['權限代號'] == 3]['姓名'].tolist()
print("品保員姓名:", 品保員_姓名)
