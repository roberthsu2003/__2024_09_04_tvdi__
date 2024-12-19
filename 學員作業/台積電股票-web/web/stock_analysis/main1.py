import pandas as pd
import numpy as np
import requests
import tkinter as tk
from ttkthemes import ThemedTk
from tkinter import ttk
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import outsources
import datasource
import mplfinance


class Window(ThemedTk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title("Stock Analysis")
        #==========STYLE===========
        style = ttk.Style(self)
        style.configure('TopFrame.TLabel',font=('Helvetica',20))
        style.configure('All.TButton',font=('Helvetica',14))
        #==========END style============
        
        #===========RightFrame=============
        self.rightFrame= ttk.Frame(self,borderwidth=2,relief='groove')

        #添加圖表
        # figure = plt.Figure(figsize =(5,4),dpi=100)
        # ax = figure.add_subplot(111)
        # ax.plot([1,2,3,4,5],[10,20,30,45])
        # ax.set_title('股票分析')

        # canvas = FigureCanvasTkAgg(figure,rightFrame)
        # canvas.get_tk_widget().pack(fill='both',expand=True)
        
        self.rightFrame.pack(side='right',fill='both',expand=True,padx=10,pady=10)
        #=========RightFrame END===========

       
        
        #===========leftFrame=============
        self.leftFrame = ttk.Frame(self)

                #==TOPFRAME=====
        self.topFrame = ttk.Frame(self.leftFrame)
        ttk.Label(self.topFrame,text='台積電股票預測',style='TopFrame.TLabel',borderwidth=2,relief='groove').pack(pady=10)
        self.icon_button = outsources.ImageButton(self.topFrame,command=self.sign )
        self.icon_button.pack(pady=7,side='right',padx=5)
        ttk.Label(self.topFrame,text=' 起始數據: 2020-01-01',style='TopFrame.TLabel',borderwidth=2,relief='groove').pack(ipadx=5,pady=10)
        self.topFrame.pack(fill='x')
                #==TOPFRAME END=====
           #=== 分析方法===
        analysisFrame = ttk.Frame(self.leftFrame)
        self.linear_btn = ttk.Button(analysisFrame,text='線性回歸分析',style='All.TButton',command=datasource.linear_regression)
        self.linear_btn.grid(row=0,column=0,padx=5,pady=5)
        self.linear_btn = ttk.Button(analysisFrame,text='RSI',style='All.TButton')
        self.linear_btn.grid(row=0,column=1,padx=5,pady=5)
        self.linear_btn = ttk.Button(analysisFrame,text='MACD',style='All.TButton')
        self.linear_btn.grid(row=1,column=0,padx=5,pady=5)
        self.linear_btn = ttk.Button(analysisFrame,text='MA',style='All.TButton')
        self.linear_btn.grid(row=1,column=1,padx=5,pady=5)

        analysisFrame.pack(fill='x',pady=10)

           #=== 分析方法end===
            #===預測分析=====
        self.resultFrame = ttk.Frame(self.leftFrame)
        ttk.Label(self.resultFrame,text='預測分析',borderwidth=2,relief='groove',style='TopFrame.TLabel').grid()
        ttk.Label(self.resultFrame,text='明日股價',borderwidth=2,relief='groove',style='TopFrame.TLabel').grid(row=0,column=0,padx=5,pady=5)
        self.result_entry = ttk.Entry(self.resultFrame)
        
        self.result_entry.grid(row=0,column=1,padx=15,pady=5)
        self.resultFrame.pack(fill='x', pady=10)
                #=== 預測分析 end===

           


        self.leftFrame.pack(side='left',fill='y',padx=10,pady=10)


        #=========leftFrame END===========



    def sign(self):
        print("Button clicked")






def main():
    window= Window(theme='arc')
    window.mainloop()


if __name__ == '__main__':
    main()

