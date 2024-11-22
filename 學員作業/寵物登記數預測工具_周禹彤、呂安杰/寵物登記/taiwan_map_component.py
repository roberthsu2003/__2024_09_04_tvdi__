import tkinter as tk
from tkinter import ttk
import json

class TaiwanMap(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        # 建立 SVG Canvas
        self.canvas = tk.Canvas(self, width=300, height=400, bg='white')
        self.canvas.pack(fill='both', expand=True)
        
        # 載入台灣地圖資料
        with open('taiwan_map.json', 'r') as f:
            self.taiwan_data = json.load(f)
        
        self.county_items = {}
        self._create_map()
        
    def _create_map(self):
        # 建立基本的地圖形狀
        counties = self.taiwan_data["objects"]["map"]["geometries"]
        scale_factor = 3  # 縮放因子
        
        # 計算相對座標
        min_x = 118.145
        min_y = 21.895
        max_x = 124.560
        max_y = 26.385
        
        width = (max_x - min_x) * scale_factor
        height = (max_y - min_y) * scale_factor
        
        # 為每個縣市創建多邊形
        for county in counties:
            name = county["properties"]["name"]
            coordinates = county["geometry"]["coordinates"][0]
            
            # 轉換座標
            scaled_coords = []
            for point in coordinates:
                x = (point[0] - min_x) * scale_factor * 100
                y = (point[1] - min_y) * scale_factor * 100
                scaled_coords.extend([x, y])
            
            # 創建多邊形
            item = self.canvas.create_polygon(
                scaled_coords,
                fill='#90EE90',  # 淺綠色
                outline='white',
                width=1,
                tags=name
            )
            self.county_items[name] = item
            
            # 添加滑鼠事件
            self.canvas.tag_bind(name, '<Enter>', self._on_enter)
            self.canvas.tag_bind(name, '<Leave>', self._on_leave)
    
    def _on_enter(self, event):
        # 滑鼠進入事件
        county = self.canvas.gettags(self.canvas.find_closest(event.x, event.y))[0]
        self.canvas.itemconfig(self.county_items[county], fill='#228B22')  # 深綠色
        
    def _on_leave(self, event):
        # 滑鼠離開事件
        county = self.canvas.gettags(self.canvas.find_closest(event.x, event.y))[0]
        self.canvas.itemconfig(self.county_items[county], fill='#90EE90')  # 淺綠色
        
    def highlight_county(self, county):
        # 重置所有縣市顏色
        for item in self.county_items.values():
            self.canvas.itemconfig(item, fill='#90EE90')
        
        # 高亮選中的縣市
        if county in self.county_items:
            self._animate_highlight(county)
            
    def _animate_highlight(self, county):
        if not hasattr(self, 'animation_step'):
            self.animation_step = 0
        
        colors = ['#228B22', '#32CD32']  # 深綠色和淺綠色交替
        
        def animate():
            if self.animation_step < 6:  # 動畫進行3次
                color = colors[self.animation_step % 2]
                self.canvas.itemconfig(self.county_items[county], fill=color)
                self.animation_step += 1
                self.after(200, animate)
            else:
                self.animation_step = 0
                self.canvas.itemconfig(self.county_items[county], fill='#228B22')
                
        animate()