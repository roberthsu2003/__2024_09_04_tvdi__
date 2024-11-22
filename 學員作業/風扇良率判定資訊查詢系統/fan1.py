import tkinter as tk
from tkinter import ttk
import pandas as pd
import csv

# 读取CSV文件，获取Plant、Workstation Code和Code数据
 # 请替换为你的实际路径
df = pd.read_csv('Factoryworkstation.csv')
# print(df)  # 打印数据框以检查内容
# 提取Plant和Workstation Code列，去除重复值
plant_list = df['Plant'].dropna().unique().tolist()
Code_list = df['Code'].dropna().unique().tolist()
WorkstationCode_list = df['Workstation Code'].dropna().unique().tolist()

# print(plant_list)
# print(WorkstationCode_list)
# print(Code_list)

    # 讀取CSV檔案
data = pd.read_csv('virtual_data_with_permissions.csv')

    # 根據權限代號過濾各角色
roles = {
        "製造者": data[data['權限代號'] == 1].set_index('ID')['姓名'].to_dict(),
        "組長": data[data['權限代號'] == 2].set_index('ID')['姓名'].to_dict(),
        "品保員": data[data['權限代號'] == 3].set_index('ID')['姓名'].to_dict(),
    }