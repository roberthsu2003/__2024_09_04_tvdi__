import tkinter as tk
from tkinter import ttk

class SitenameFrame(tk.Frame):
    def __init__(self, master, distnames, radio_controll, **kwargs):
        super().__init__(master, **kwargs)
        self.radio_controll = radio_controll
        self.selected_dist = tk.StringVar()  # 用來保存選擇的區域
        
        # 檢查傳遞過來的 distnames 是否為空
        if not distnames:
            print("無區域資料可顯示！")
            return
        
        # 確保將 radiobutton 分為兩排顯示
        row = 0
        col = 0
        max_columns = 2  # 每行最多顯示 2 個 radio button
        
        # 創建並顯示區域的 radio buttons
        for dist in distnames:
            radio_button = ttk.Radiobutton(self, text=dist, value=dist, variable=self.selected_dist, command=self.on_radio_button_click)
            radio_button.grid(row=row, column=col, sticky="w", padx=5, pady=5)
            
            # 根據列的數量來調整 row 和 column
            col += 1
            if col >= max_columns:
                col = 0
                row += 1

    def on_radio_button_click(self):
        # 當選擇某個區域時，觸發傳入的 radio_controll 回調
        selected_dist = self.selected_dist.get()
        if selected_dist:
            self.radio_controll(selected_dist)
