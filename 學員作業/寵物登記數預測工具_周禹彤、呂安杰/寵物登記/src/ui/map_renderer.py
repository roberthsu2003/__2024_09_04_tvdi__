import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, Optional
import tkintermapview

class TaiwanMapRenderer(ttk.Frame):
    def __init__(self, master: tk.Widget, data_manager, height=400):
        super().__init__(master)
        self.data_manager = data_manager
        self.on_county_select: Optional[Callable[[str], None]] = None
        
        self.map_widget = tkintermapview.TkinterMapView(self, width=400, height=height)
        self.map_widget.pack(fill="both", expand=True)
        
        self.map_widget.set_tile_server("https://wmts.nlsc.gov.tw/wmts/EMAP/default/EPSG:3857/{z}/{y}/{x}", max_zoom=19)
        self.map_widget.set_position(23.97565, 120.973882)
        self.map_widget.set_zoom(7)
        
        self.markers = {}
        self._create_markers()
        
        self.selected_county = None
        self.selected_marker = None

    def _create_markers(self):
        county_positions = {
            "臺北市": (25.033, 121.565),
            "新北市": (25.037, 121.437),
            "桃園市": (24.989, 121.313),
            "臺中市": (24.148, 120.674),
            "臺南市": (23.000, 120.227),
            "高雄市": (22.627, 120.301),
            "基隆市": (25.128, 121.742),
            "新竹市": (24.814, 120.968),
            "新竹縣": (24.839, 121.013),
            "苗栗縣": (24.560, 120.821),
            "彰化縣": (24.052, 120.516),
            "南投縣": (23.961, 120.988),
            "雲林縣": (23.709, 120.431),
            "嘉義市": (23.480, 120.449),
            "嘉義縣": (23.452, 120.256),
            "屏東縣": (22.552, 120.549),
            "宜蘭縣": (24.702, 121.738),
            "花蓮縣": (23.987, 121.601),
            "臺東縣": (22.797, 121.144),
            "澎湖縣": (23.571, 119.579),
            "金門縣": (24.449, 118.376),
            "連江縣": (26.151, 119.950)
        }

        for county, pos in county_positions.items():
            marker = self.map_widget.set_marker(
                pos[0], pos[1], 
                text=county,
                command=lambda c=county: self._on_marker_click(c)
            )
            self.markers[county] = marker

    def _on_marker_click(self, county):
        if self.on_county_select:
            self.on_county_select(county)

    def select_county(self, county_name: str):
        if county_name in self.markers:
            if self.selected_marker:
                self.selected_marker.set_text(self.selected_county)
            
            marker = self.markers[county_name]
            marker.set_text("🔴 " + county_name)
            
            self.map_widget.set_position(
                marker.position[0], 
                marker.position[1]
            )
            self.map_widget.set_zoom(9)
            
            self.selected_county = county_name
            self.selected_marker = marker
