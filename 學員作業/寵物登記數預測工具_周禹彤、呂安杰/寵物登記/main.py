import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pet_datasource import PetDataSource
import json
import numpy as np
import tkintermapview

class TaiwanMap(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        # 創建地圖元件
        self.map_view = tkintermapview.TkinterMapView(self, width=300, height=400, corner_radius=0)
        self.map_view.pack(fill='both', expand=True)
        
        # 設置地圖中心和縮放等級
        self.map_view.set_position(23.6, 121.0) # 台灣大致中心
        self.map_view.set_zoom(8)
        
        # 添加標記
        self.county_markers = {}
        self.add_county_markers()
        
    def add_county_markers(self):
        # 在地圖上添加每個縣市的標記
        counties = [
            ("臺北市", 25.033, 121.565),
            ("新北市", 24.983, 121.467),
            ("桃園市", 24.99, 121.302),
            ("臺中市", 24.143, 120.679),
            ("臺南市", 22.99, 120.209),
            ("高雄市", 22.62, 120.308),
            ("基隆市", 25.133, 121.733),
            ("新竹市", 24.8, 120.967),
            ("新竹縣", 24.833, 121.033),
            ("苗栗縣", 24.567, 120.817),
            ("彰化縣", 24.083, 120.517),
            ("南投縣", 23.917, 120.683),
            ("雲林縣", 23.75, 120.533),
            ("嘉義市", 23.483, 120.45),
            ("嘉義縣", 23.5, 120.3),
            ("屏東縣", 22.683, 120.483),
            ("臺東縣", 22.75, 121.15),
            ("花蓮縣", 23.983, 121.6),
            ("宜蘭縣", 24.767, 121.75),
            ("澎湖縣", 23.567, 119.567),
            ("金門縣", 24.433, 118.317),
            ("連江縣", 26.15, 119.95)
        ]
        
        for county, lat, lon in counties:
            marker = self.map_view.set_marker(lat, lon, text=county)
            self.county_markers[county] = marker
            
    def highlight_county(self, county):
    # 高亮顯示選中的縣市
        if county in self.county_markers:
            self.county_markers[county].set_text("🔴 " + county)
            self.county_markers[county].set_icon_image("red_circle")
        
        # 重置其他縣市標記
        for other_county, marker in self.county_markers.items():
            if other_county != county:
                marker.set_text(other_county)
                marker.set_icon_image("black_circle")

    
class PetAnalysisWindow(ThemedTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('寵物登記與絕育分析')
        self.geometry('1400x900')
        self.datasource = PetDataSource()
        
        # 設定中文字型
        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
        plt.rcParams['axes.unicode_minus'] = False
        
        # Style configuration
        style = ttk.Style(self)
        style.configure('TopFrame.TLabel', font=('Microsoft JhengHei', 20))

        # 設定關閉視窗事件
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self._create_widgets()

    def on_closing(self):
        """處理視窗關閉事件"""
        plt.close('all')
        self.quit()
        self.destroy()
        
    def _create_widgets(self):
        # Top Frame
        top_frame = ttk.Frame(self)
        ttk.Label(top_frame, text='寵物登記與絕育統計分析', style='TopFrame.TLabel').pack()
        top_frame.pack(padx=20, pady=20)
        
        # Main Content Frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left Frame for Controls and Map
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side='left', fill='y', padx=10)
        
        # Selector Frame
        selector_frame = ttk.LabelFrame(left_frame, text="選擇縣市", padding=5)
        selector_frame.pack(fill='x', pady=5)
        
        # County Combobox
        counties = self.datasource.get_counties()
        self.selected_county = tk.StringVar()
        county_frame = ttk.Frame(selector_frame)
        county_frame.pack(fill='x', pady=5)
        ttk.Label(county_frame, text="縣市:").pack(side='left')
        county_cb = ttk.Combobox(county_frame, textvariable=self.selected_county, values=counties, state='readonly', width=15)
        self.selected_county.set(counties[0])
        county_cb.pack(side='left', padx=5)
        
        # 在左下角添加台灣地圖
        self.taiwan_map = TaiwanMap(left_frame)
        self.taiwan_map.pack(side='bottom', fill='both', expand=True, pady=10)
        
        # 綁定選擇事件
        self.selected_county.trace('w', self._on_county_selected)
        
        # Right Frame for Data Display
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side='right', fill='both', expand=True)
        
        # Tree View
        tree_frame = ttk.LabelFrame(right_frame, text="詳細資料", padding=10)
        tree_frame.pack(fill='x', pady=5)
        
        # Add scrollbar
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side='right', fill='y')
        
        columns = ('year', 'county', 'registrations', 'deregistrations', 'neutered', 'rate')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=self.tree.yview)
        
        self.tree.heading('year', text='年份')
        self.tree.heading('county', text='縣市')
        self.tree.heading('registrations', text='登記數')
        self.tree.heading('deregistrations', text='註銷數')
        self.tree.heading('neutered', text='絕育數')
        self.tree.heading('rate', text='絕育率(%)')
        
        for col in columns:
            self.tree.column(col, width=100, anchor='center')
        
        self.tree.pack(fill='x')
        
        # Chart Frame
        self.chart_frame = ttk.LabelFrame(right_frame, text="圖表分析", padding=10)
        self.chart_frame.pack(fill='both', expand=True, pady=5)
        
        self.update_data()
        
    def _on_county_selected(self, *args):
        """當選擇縣市時更新地圖和數據"""
        selected = self.selected_county.get()
        self.taiwan_map.highlight_county(selected)
        self.update_data()
        
    def update_data(self, event=None):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Update tree view based on selected county
        county_data = self.datasource.get_county_data(self.selected_county.get())
        for record in county_data:
            self.tree.insert('', 'end', values=record)
        
        # Update chart
        self.update_chart()
        
    def update_chart(self):
        try:
            # Clear existing chart
            for widget in self.chart_frame.winfo_children():
                widget.destroy()
            
            # 創建新圖表，調整大小和內邊距
            fig = plt.figure(figsize=(14, 10))
            
            # 創建子圖，調整間距
            gs = plt.GridSpec(2, 2, height_ratios=[1.5, 1])
            gs.update(hspace=0.8, wspace=0.3)
            
            # Get data for selected county
            county_data = self.datasource.get_county_data(self.selected_county.get())
            years = [str(record[0]) for record in reversed(county_data)]
            registrations = [record[2] for record in reversed(county_data)]
            deregistrations = [record[3] for record in reversed(county_data)]
            neutered = [record[4] for record in reversed(county_data)]
            rates = [record[5] for record in reversed(county_data)]
            
            # 1. Registration and Deregistration Trend
            ax1 = fig.add_subplot(gs[0, :])
            ax1.plot(years, registrations, marker='o', color='blue', linewidth=2, label='登記數')
            ax1.plot(years, deregistrations, marker='s', color='red', linewidth=2, label='註銷數')
            ax1.set_title(f'{self.selected_county.get()} 寵物登記與註銷趨勢', fontsize=12, pad=15)
            ax1.set_xlabel('年份', fontsize=10, labelpad=10)
            ax1.set_ylabel('數量', fontsize=10, labelpad=10)
            ax1.grid(True, linestyle='--', alpha=0.7)
            ax1.legend(loc='upper right')
            
            plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
            
            # 2. Neutering Rate Trend
            ax2 = fig.add_subplot(gs[1, 0])
            ax2.plot(years, rates, marker='o', color='green', linewidth=2)
            ax2.set_title(f'{self.selected_county.get()} 絕育率趨勢', fontsize=12, pad=15)
            ax2.set_xlabel('年份', fontsize=10, labelpad=10)
            ax2.set_ylabel('絕育率 (%)', fontsize=10, labelpad=10)
            ax2.grid(True, linestyle='--', alpha=0.7)
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
            
            # 3. Neutering vs Registration Ratio
            ax3 = fig.add_subplot(gs[1, 1])
            ratio = [n/r*100 for n, r in zip(neutered, registrations)]
            ax3.plot(years, ratio, marker='o', color='purple', linewidth=2)
            ax3.set_title(f'{self.selected_county.get()} 絕育數與登記數比率', fontsize=12, pad=15)
            ax3.set_xlabel('年份', fontsize=10, labelpad=10)
            ax3.set_ylabel('比率 (%)', fontsize=10, labelpad=10)
            ax3.grid(True, linestyle='--', alpha=0.7)
            plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')
            
            fig.subplots_adjust(left=0.1, right=0.95, bottom=0.2, top=0.95)
            
            # Embed chart in window
            canvas = FigureCanvasTkAgg(fig, self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            
        except Exception as e:
            print(f"Error updating chart: {e}")

def main():
    window = PetAnalysisWindow(theme="arc")
    window.mainloop()

if __name__ == '__main__':
    main()