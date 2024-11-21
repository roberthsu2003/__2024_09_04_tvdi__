import tkinter as tk
from tkinter import ttk, messagebox

# 主應用程式框架
class StockDataAnalysisApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("法人歷史買賣超數據查詢系統")
        self.geometry("1000x600")

        # 設置左側導覽區和右側資料顯示區
        self.create_left_panel()
        self.create_right_panel()

    # 左側導覽區
    def create_left_panel(self):
        left_panel = tk.Frame(self, width=250, bg="lightgray")
        left_panel.pack(side="left", fill="y")

        # Radiobutton選擇功能
        self.function_var = tk.StringVar(value="selection1")
        tk.Label(left_panel, text="選擇功能", bg="lightgray").pack(pady=10)
        tk.Radiobutton(left_panel, text="功能保留", variable=self.function_var, value="selection1", bg="lightgray").pack(anchor="w")
        tk.Radiobutton(left_panel, text="長期選股參考 - 法人歷史買賣超數據統計", variable=self.function_var, value="selection2", bg="lightgray").pack(anchor="w")

        # 法人下拉選單
        tk.Label(left_panel, text="法人選擇", bg="lightgray").pack(pady=10)
        self.institution_var = tk.StringVar(value="外資投信")
        institution_options = ["外資投信", "外資自營", "自營", "投信", "三大法人加總", "全股市"]
        ttk.Combobox(left_panel, textvariable=self.institution_var, values=institution_options).pack(fill="x")

        # 時間範圍下拉選單
        tk.Label(left_panel, text="時間範圍", bg="lightgray").pack(pady=10)
        self.time_range_var = tk.StringVar(value="近一年")
        time_range_options = ["近一月", "近一年"]
        ttk.Combobox(left_panel, textvariable=self.time_range_var, values=time_range_options).pack(fill="x")

        # 時間跨度下拉選單
        tk.Label(left_panel, text="時間跨度", bg="lightgray").pack(pady=10)
        self.time_span_var = tk.StringVar(value="月")
        time_span_options = ["近一週", "月"]
        ttk.Combobox(left_panel, textvariable=self.time_span_var, values=time_span_options).pack(fill="x")

        # 前幾大買超股票下拉選單
        tk.Label(left_panel, text="前幾大買超股票", bg="lightgray").pack(pady=10)
        self.top_n_var = tk.StringVar(value="Top5")
        top_n_options = ["Top1", "Top5"]
        ttk.Combobox(left_panel, textvariable=self.top_n_var, values=top_n_options).pack(fill="x")

        # 查詢按鈕
        tk.Button(left_panel, text="查詢", command=self.query_data).pack(pady=20)

    # 右側資料顯示區
    def create_right_panel(self):
        self.right_panel = tk.Frame(self, bg="white")
        self.right_panel.pack(side="right", fill="both", expand=True)

        # 預設提示文字
        self.result_label = tk.Label(self.right_panel, text="請選擇查詢條件並按下查詢按鈕", bg="white", font=("Arial", 16))
        self.result_label.pack(pady=20)

    # 查詢數據並更新右側區域（僅 GUI 顯示功能示例）
    def query_data(self):
        # 從選項中取得使用者輸入
        selected_function = self.function_var.get()
        institution = self.institution_var.get()
        time_range = self.time_range_var.get()
        time_span = self.time_span_var.get()
        top_n = self.top_n_var.get()

        # 驗證選項
        if selected_function != "selection2":
            messagebox.showinfo("提示", "請選擇『長期選股參考』功能")
            return

        # 在此處加入處理和查詢邏輯
        self.result_label.config(text=f"顯示結果\n法人: {institution}\n時間範圍: {time_range}\n時間跨度: {time_span}\n前幾大: {top_n}")
        
        # 清空之前的查詢結果，顯示新的圖表與表格
        for widget in self.right_panel.winfo_children():
            widget.destroy()

        # 模擬顯示查詢的表格與圖表結果
        self.result_label = tk.Label(self.right_panel, text=f"查詢結果\n法人: {institution}\n時間範圍: {time_range}\n時間跨度: {time_span}\n前幾大: {top_n}", font=("Arial", 14), bg="white")
        self.result_label.pack(pady=20)

# 啟動應用程式
if __name__ == "__main__":
    app = StockDataAnalysisApp()
    app.mainloop()