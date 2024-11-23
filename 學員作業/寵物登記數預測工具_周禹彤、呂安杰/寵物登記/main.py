import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from src.ui.analysis_view import AnalysisView
from src.data.data_source import DataManager

def main():
    root = ThemedTk(theme="arc")
    root.title('寵物登記與絕育分析')
    root.geometry('1400x900')
    
    data_manager = DataManager()
    view = AnalysisView(root, data_manager)
    view.pack(fill='both', expand=True)
    
    root.mainloop()

if __name__ == '__main__':
    main()