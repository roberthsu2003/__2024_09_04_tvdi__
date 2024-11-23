import tkinter as tk
from tkinter import ttk

'''老師的tree'''
# =====Treeview =====
                #define columns
columns = ('date', 'county','sitename', 'aqi', 'pm25','status','lat','lon')

self.tree = ttk.Treeview(rightFrame, columns=columns, show='headings')
self.tree.bind('<<TreeviewSelect>>', self.item_selected)
# define headings
self.tree.heading('date', text='日期')
self.tree.heading('county', text='縣市')
self.tree.heading('sitename', text='站點')
self.tree.heading('aqi', text='AQI')
self.tree.heading('pm25', text='PM25')
self.tree.heading('status',text='狀態')
self.tree.heading('lat', text='緯度')
self.tree.heading('lon', text='經度')

self.tree.column('date', width=150,anchor="center")
self.tree.column('county', width=80,anchor="center")
self.tree.column('sitename', width=80,anchor="center")
self.tree.column('aqi', width=50,anchor="center")
self.tree.column('pm25', width=50,anchor="center")
self.tree.column('status', width=50,anchor="center")
self.tree.column('lat', width=100,anchor="center")
self.tree.column('lon', width=100,anchor="center")

self.tree.pack(side='top')