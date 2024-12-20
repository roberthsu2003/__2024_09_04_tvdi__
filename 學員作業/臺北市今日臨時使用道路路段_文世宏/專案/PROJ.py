from tkinter import ttk
import tkinter as tk
from ttkthemes import ThemedTk
from tkinter.messagebox import showinfo

import functoins 
import view
from pandas import DataFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Window(ThemedTk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('登入')
        self.resizable(True, True)
        #==============style===============
        style = ttk.Style(self)
        style.configure('TopFrame.TLabel',font=('Helvetica',20))
        #============end style===============

        #==============top Frame==================
        topFrame = ttk.Frame(self)
        ttk.Label(topFrame,text='台北市今日使用道路',style='TopFrame.TLabel').pack()
        topFrame.pack(padx=20,pady=20)
        #==============end topFrame===============

        #==============bottomFrame===============
        bottomFrame = ttk.Frame(self,padding=[10,10,10,10])
        #==============combobxfrmae===============
        self.selectedFrame= ttk.Frame(self,padding=[10,10,10,10])
        #combobox選擇城市      
        counties = functoins.get_district()
        self.selected_district = tk.StringVar()
        sitenames_cb = ttk.Combobox(self.selectedFrame, textvariable=self.selected_district,values=counties,state='readonly')
        self.selected_district.set('請選擇城市')
        sitenames_cb.bind('<<ComboboxSelected>>', self.cb_click)
        sitenames_cb.pack(anchor='n',pady=10)

        self.sitenameFrame = None 

        self.selectedFrame.pack(side='left',padx=(20,0))
    #===========================end selected frame========================================
    #===========================right frame===============================================
        rightFrame = ttk.LabelFrame(bottomFrame,text="道路資訊",padding=[10,10,10,10])
        #建立ㄘㄨ一ㄅㄧㄨˋ
        # define columns
        columns = ('date', 'address', 'lat', 'lon')

        self.tree = ttk.Treeview(rightFrame, columns=columns, show='headings')
        # self.tree.bind('<<TreeviewSelect>>', self.item_selected)
        
        # define headings
        self.tree.heading('date', text='日期')
        self.tree.heading('address', text='地址')
        self.tree.heading('lat', text='緯度')
        self.tree.heading('lon', text='經度')

        self.tree.column('date', width=100,anchor="center")
        self.tree.column('address', width=500,anchor="w")
        self.tree.column('lat', width=100,anchor="center")
        self.tree.column('lon', width=100,anchor="center")

        self.tree.pack(side='top')

        rightFrame.pack(side='right')
    #===========================end right frame======================================
        bottomFrame.pack(padx=20,pady=20)
    #============================end bottom frame=====================================        

    def cb_click(self,event:str):
            '''
            - 此method是傳遞給treeview實體
            - 當cb被選取時,會連動執行此method
            Parameter:
                selected_district:str -> 這是被選取的站點名稱
            '''
            selected = self.selected_district.get()
            addresses = functoins.get_selected_data(district=selected)
            #清空treeview 填進新的資料
            for children in self.tree.get_children():
                self.tree.delete(children)      
            selected_data = functoins.get_selected_data(selected)
            for record in selected_data:
                self.tree.insert("", "end", values=record)

            #currentedit
            # dataframe:DataFrame = datasource.get_plot_data(sitename=selected_sitename)
            # axes = dataframe.plot()
            # figure = axes.get_figure()
            # if self.canvas:
            #     self.canvas.get_tk_widget().destroy()
            # self.canvas = FigureCanvasTkAgg(figure, master = self.plotFrame)
            # self.canvas.draw()
            # self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True, pady = (20,10))

    # def item_selected(self,event):
    #     for select_item in self.tree.selection():
    #         record = self.tree.item(select_item)
    #         dialog = view.MyCustomDialog(parent = self, title = f'{record["values"][1]} - {record["values"][2]}', record = record['values'])



















def main():
    window = Window(theme="arc")
    window.mainloop()

if __name__ == '__main__':
    main()