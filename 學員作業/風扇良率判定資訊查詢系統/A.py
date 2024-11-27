

import pandas as pd

# 讀取CSV檔案
csv_file = 'orders_large.csv'  # 替換為你的CSV檔案路徑
df = pd.read_csv(csv_file)

# 設定查找條件
target_date = '2024-06-18'
target_order_id = 'ORD9700'

# 查找符合條件的行
result = df[(df['Date'] == target_date) & (df['OrderID'] == target_order_id)]

# 顯示結果
if not result.empty:
    print(f"Product: {result['Product'].iloc[0]}")
else:
    print("")

target_date = '2024-06-18'
target_order_id = 'ORD9700'

# 查找符合條件的行
result = df[(df['Date'] == target_date) & (df['OrderID'] == target_order_id)]

# 顯示結果
if not result.empty:
    print(f"Quantity: {result['Quantity'].iloc[0]}")
else:
    print("")
