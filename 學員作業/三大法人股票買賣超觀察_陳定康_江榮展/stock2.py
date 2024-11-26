import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator  # 引入 MaxNLocator

DATA_PATH = "./data/"

class StockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("國內外投信股票買賣查詢系統")

        # Left Navigation
        self.nav_frame = tk.Frame(root)
        self.nav_frame.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(self.nav_frame, text="選擇股票").pack(anchor="w")
        self.stock_combobox = ttk.Combobox(self.nav_frame, state="readonly")
        self.stock_combobox.pack(fill="x")
        self.stock_combobox.bind("<<ComboboxSelected>>", self.display_data)

        # Right Display Area
        self.display_frame = tk.Frame(root)
        self.display_frame.pack(side="right", fill="both", expand=True)

        # Table Area
        self.table_frame = tk.Frame(self.display_frame)
        self.table_frame.pack(side="top", fill="x", padx=10, pady=5)
        tk.Label(self.table_frame, text="當月買賣股數", font=("Arial", 14)).pack(anchor="w")

        # Scrollable Treeview
        self.scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")
        self.table = ttk.Treeview(
            self.table_frame,
            columns=["Month", "All Investors", "Foreign Agency", "Agency"],
            show="headings",
            yscrollcommand=self.scrollbar.set,
        )
        self.scrollbar.config(command=self.table.yview)

        for col, name in zip(
            ["Month", "All Investors", "Foreign Agency", "Agency"],
            ["Month", "All Investors", "Foreign Agency", "Domestic Agency"],
        ):
            self.table.heading(col, text=name)
            self.table.column(col, anchor="center" if col == "Month" else "e", width=150)
        self.table.pack(fill="x", expand=True)

        # Plot Area
        self.plot_frame = tk.Frame(self.display_frame)
        self.plot_frame.pack(side="bottom", fill="both", expand=True)
        self.canvas = None

        # Load data and initialize
        self.data = self.load_data()
        self.stock_combobox["values"] = list(self.data["all_trading"].columns)
        self.stock_combobox.set("2330 台積電")
        self.display_data()

    def load_data(self):
        """
        Load data from CSV files
        """
        return {
            "all_trading": pd.read_csv(f"{DATA_PATH}all_trading.csv", index_col=0, parse_dates=True),
            "foreign_agency_trading": pd.read_csv(f"{DATA_PATH}foreign_agency_trading.csv", index_col=0, parse_dates=True),
            "agency_trading": pd.read_csv(f"{DATA_PATH}agency_trading.csv", index_col=0, parse_dates=True),
        }

    def process_monthly_data(self, stock):
        """
        Process data to calculate monthly sums
        """
        monthly_data = pd.DataFrame({
            "All Investors": self.data["all_trading"][stock],
            "Foreign Agency": self.data["foreign_agency_trading"][stock],
            "Agency": self.data["agency_trading"][stock],
        }).fillna(0)

        # Resample by month and sum
        monthly_data = monthly_data.resample("ME").sum()

        # Sort by newest date
        monthly_data = monthly_data.sort_index(ascending=False)

        # Format month and numeric data
        monthly_data.index = monthly_data.index.strftime("%Y-%m")  # Format index as "YYYY-MM"
        monthly_data = monthly_data.round().astype(int)  # Round to integers
        monthly_data["All Investors"] = monthly_data["All Investors"].apply(lambda x: f"{x:,}")
        monthly_data["Foreign Agency"] = monthly_data["Foreign Agency"].apply(lambda x: f"{x:,}")
        monthly_data["Agency"] = monthly_data["Agency"].apply(lambda x: f"{x:,}")

        return monthly_data.reset_index().values.tolist(), monthly_data

    def plot_data(self, data):
        """
        Plot stock transactions trend
        """
        # 確保數據按照年月升序排列
        data = data.sort_index()

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.plot(data.index, data["All Investors"].str.replace(",", "").astype(int), label="All Investors", marker="o")
        ax.plot(data.index, data["Foreign Agency"].str.replace(",", "").astype(int), label="Foreign Agency", marker="x")
        ax.plot(data.index, data["Agency"].str.replace(",", "").astype(int), label="Domestic Agency", marker="*")

        ax.set_title("Monthly Stock Transactions Trend", fontsize=16)
        ax.set_xlabel("Month", fontsize=12)
        ax.set_ylabel("Transaction Volume", fontsize=12)
        ax.legend(fontsize=10)
        ax.grid(True)

        # 設定 X 軸顯示的標籤間距和旋轉
        ax.xaxis.set_major_locator(MaxNLocator(integer=True, prune="both", nbins=20))  # 限制最多顯示 20 個標籤
        plt.xticks(rotation=45)  # 旋轉 X 軸標籤以避免重疊

        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def display_data(self, event=None):
        """
        Display data for the selected stock
        """
        stock = self.stock_combobox.get()
        table_data, plot_data_values = self.process_monthly_data(stock)

        # Update table
        for row in self.table.get_children():
            self.table.delete(row)
        for row in table_data:
            self.table.insert("", "end", values=row)

        # Update plot
        self.plot_data(plot_data_values)


if __name__ == "__main__":
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()