import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 設置中文字體
rcParams['font.family'] = 'Microsoft JhengHei'  # 微軟正黑體（或替換為系統中的其他中文字體）

# Step 1: 獲取台積電股票數據
ticker = "2330.TW"  # 台積電代碼
data = yf.download(ticker, start="2023-01-01", end="2024-11-13")

# Step 2: 計算 RSI
window = 14  # RSI 計算窗口

# 計算每日價格變化
delta = data['Close'].diff()

# 分別計算上漲和下跌數據
gain = delta.where(delta > 0, 0)  # 上漲數據
loss = -delta.where(delta < 0, 0)  # 下跌數據

# 計算平均上漲與平均下跌
avg_gain = gain.rolling(window=window).mean()
avg_loss = loss.rolling(window=window).mean()

# 計算 RS 和 RSI
rs = avg_gain / avg_loss
data['RSI'] = 100 - (100 / (1 + rs))

# Step 3: 繪製圖形
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# 設定背景顏色為灰色
axes[0].set_facecolor('lightgrey')
axes[1].set_facecolor('lightgrey')

# 繪製收盤價
axes[0].plot(data['Close'], label='Close Price', color='blue')
axes[0].set_title('台積電收盤價', fontsize=14)
axes[0].set_xlabel('日期', fontsize=12)  # X 軸標籤
axes[0].set_ylabel('價格 (TWD)', fontsize=12)  # Y 軸標籤
axes[0].legend()

# 繪製 RSI
axes[1].plot(data['RSI'], label='RSI', color='purple')
axes[1].axhline(70, color='red', linestyle='--',
                linewidth=0.5, label='超買區 (70)')  # 超買區
axes[1].axhline(30, color='green', linestyle='--',
                linewidth=0.5, label='超賣區 (30)')  # 超賣區
axes[1].set_title('RSI 指標', fontsize=14)
axes[1].set_xlabel('日期', fontsize=12)  # X 軸標籤
axes[1].set_ylabel('RSI 值', fontsize=12)  # Y 軸標籤
axes[1].legend()

# 調整佈局避免重疊
plt.tight_layout()

# 顯示圖形
plt.show()
