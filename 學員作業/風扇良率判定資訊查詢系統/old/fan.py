import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter.messagebox import showinfo
import pandas as pd
import fan1 as f


class Window(ThemedTk):
    def __init__(self, *args, **kwargs):
        super().__init__()
        #===============style============================
        self.title('風扇貼標正確判斷')#類似網頁標題
        # self.geometry("1024x800")#給視窗寬度
        style = ttk.Style(self)
        style.configure("Topframe.Tabel",font=('Helvetica',20))#標題的形式
        font1=('標楷體',18)
        #===============style end=========================
        #===============TOP frame=========================
        topFrame =ttk.Frame(self)#創建一個div
        ttk.Label(topFrame,text='風扇貼標歪斜檢測',font=('Helvetica',40)).pack(padx=50,pady=50)
        topFrame.pack()
        #============== frame end =========================
        #============== top mid ==========================
        midFrame = ttk.Frame(self)

        Factory_LB = tk.Label(self,text="廠區:",font=font1)
        Factory_LB.pack(side="left")

        Factory_county = tk.StringVar()

        Factory_cobox = ttk.Combobox(
                self,textvariable=Factory_county,
                values=f.plant_list, 
                state="readonly",
                width=10)
        Factory_cobox.set("請選擇廠區")
        Factory_cobox.pack(side="left")
        Factory_cobox.bind("<<ComboboxSelected>>", self.Factory_county)

        workshop_LB = tk.Label(self,text="車間:",font=font1)
        workshop_LB.pack(side="left")
        workshop_county = tk.StringVar()

        workshop_cobox = ttk.Combobox(
                self,textvariable=workshop_county,
                values=f.WorkstationCode_list,
                state="readonly",
                width=10)
        workshop_cobox.set("請選擇廠區")
        workshop_cobox.pack(side="left")
        workshop_cobox.bind("<<ComboboxSelected>>", self.workshop_county)
        midFrame.pack()
        
        workstation_LB = tk.Label(self,text="工站:",font=font1)
        workstation_LB.pack(side="left")
        workstation_county = tk.StringVar()

        workstation_cobox = ttk.Combobox(
                self,textvariable=workstation_county,
                values=f.Code_list,
                state="readonly",
                width=10)
        workstation_cobox.set("請選擇工站")
        workstation_cobox.pack(side="left")
        workstation_cobox.bind("<<ComboboxSelected>>", self.workstation)
        midFrame.pack()
    def Factory_county(self,event):
        Factory_city = event.widget.get()
        print(Factory_city)


    def workshop_county(self,event):
        workshop_city = event.widget.get()
        print(workshop_city)
        
    def workstation(self,event):
        workstation_city = event.widget.get()
        print(workstation_city)
    # def update_code_options(event):
    #     df = pd.read_csv('Factoryworkstation.csv')
    #     Factory_city = event.widget.get() 
    #     workstation_city = event.widget.get()
    #     if Factory_city and workstation_city:  # 如果都已选择
    #         # 根据选择的Plant和Workstation Code，过滤出对应的Code
    #         filtered_codes = df[(df['Plant'] == Factory_city) & 
    #                             (df['Workstation Code'] == workstation_city)]['Code'].unique().tolist()
    #         workstation_city['values'] = filtered_codes  # 更新Code的选项
    #         workstation_city = event.widget.get('')  # 清空Code选择

if __name__== "__main__":
    window = Window()
    window.mainloop()

