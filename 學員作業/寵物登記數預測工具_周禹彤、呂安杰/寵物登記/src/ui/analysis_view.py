import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from .map_renderer import TaiwanMapRenderer

class AnalysisView(ttk.Frame):
    def __init__(self, master, data_manager):
        super().__init__(master)
        self.data_manager = data_manager
        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
        plt.rcParams['axes.unicode_minus'] = False
        self._create_widgets()

    def _create_widgets(self):
        # Left Frame
        left_frame = ttk.Frame(self)
        left_frame.pack(side='left', fill='y', padx=10)
        
        # Selector Frame
        selector_frame = ttk.LabelFrame(left_frame, text="選擇縣市", padding=5)
        selector_frame.pack(fill='x', pady=5)
        
        # County Combobox
        county_frame = ttk.Frame(selector_frame)
        county_frame.pack(fill='x', pady=5)
        ttk.Label(county_frame, text="縣市:").pack(side='left')
        
        self.selected_county = tk.StringVar()
        counties = self.data_manager.get_counties()
        county_cb = ttk.Combobox(
            county_frame, 
            textvariable=self.selected_county,
            values=counties,
            state='readonly',
            width=15
        )
        self.selected_county.set(counties[0])
        county_cb.pack(side='left', padx=5)
        
        # Map Frame
        map_frame = ttk.LabelFrame(left_frame, text="台灣地圖", padding=5)
        map_frame.pack(fill='both', expand=True, pady=5)
        
        # Map Renderer
        self.map_renderer = TaiwanMapRenderer(map_frame, self.data_manager)
        self.map_renderer.pack(fill='both', expand=True)
        
        # Right Frame
        right_frame = ttk.Frame(self)
        right_frame.pack(side='right', fill='both', expand=True)
        
        # Tree View
        tree_frame = ttk.LabelFrame(right_frame, text="詳細資料", padding=10)
        tree_frame.pack(fill='x', pady=5)
        
        columns = ('year', 'county', 'registrations', 'deregistrations', 'neutered', 'rate')
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            height=5
        )
        
        column_texts = ['年份', '縣市', '登記數', '註銷數', '絕育數', '絕育率(%)']
        for col, text in zip(columns, column_texts):
            self.tree.heading(col, text=text)
            self.tree.column(col, width=100, anchor='center')
        
        self.tree.pack(fill='x')
        
        # Chart Frame
        self.chart_frame = ttk.LabelFrame(right_frame, text="圖表分析", padding=10)
        self.chart_frame.pack(fill='both', expand=True, pady=5)
        
        # Bind Events
        self.selected_county.trace('w', self._on_county_selected)
        self.map_renderer.on_county_select = self._on_map_county_selected
        
        self.update_data()
    
    def _on_county_selected(self, *args):
        selected = self.selected_county.get()
        self.map_renderer.select_county(selected)
        self.update_data()
    
    def _on_map_county_selected(self, county):
        self.selected_county.set(county)
    
    def update_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        county_data = self.data_manager.get_pet_data(self.selected_county.get())
        for record in county_data:
            self.tree.insert('', 'end', values=record)
        
        self.update_chart()
    
    def update_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
            
        county_data = self.data_manager.get_pet_data(self.selected_county.get())
        if not county_data:
            return
            
        fig = plt.figure(figsize=(10, 8))
        gs = plt.GridSpec(2, 2, height_ratios=[1.5, 1])
        gs.update(hspace=0.4, wspace=0.3)
        
        self._plot_trends(fig, gs, county_data)
        
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def _plot_trends(self, fig, gs, data):
        years = [str(record[0]) for record in reversed(data)]
        registrations = [record[2] for record in reversed(data)]
        deregistrations = [record[3] for record in reversed(data)]
        neutered = [record[4] for record in reversed(data)]
        rates = [record[5] for record in reversed(data)]
        
        ax1 = fig.add_subplot(gs[0, :])
        ax1.plot(years, registrations, 'bo-', label='登記數')
        ax1.plot(years, deregistrations, 'ro-', label='註銷數')
        ax1.set_title(f'{self.selected_county.get()} 寵物登記與註銷趨勢')
        ax1.set_xlabel('年份')
        ax1.set_ylabel('數量')
        ax1.legend()
        ax1.grid(True)
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        
        ax2 = fig.add_subplot(gs[1, 0])
        ax2.plot(years, rates, 'go-')
        ax2.set_title(f'{self.selected_county.get()} 絕育率趨勢')
        ax2.set_xlabel('年份')
        ax2.set_ylabel('絕育率 (%)')
        ax2.grid(True)
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        
        ax3 = fig.add_subplot(gs[1, 1])
        ratio = [n/r*100 for n, r in zip(neutered, registrations)]
        ax3.plot(years, ratio, 'mo-')
        ax3.set_title(f'{self.selected_county.get()} 絕育數與登記數比率')
        ax3.set_xlabel('年份')
        ax3.set_ylabel('比率 (%)')
        ax3.grid(True)
        plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)