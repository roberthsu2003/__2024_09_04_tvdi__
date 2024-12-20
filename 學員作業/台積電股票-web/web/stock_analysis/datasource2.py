import yfinance as yf
import sqlite3
import pandas as pd
import datetime
from datetime import datetime, timedelta 
from tkinter import messagebox






def download_data():
    symbol = '2330.TW'
    start = '2020-01-01'
    end = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    conn = sqlite3.connect('check_data.db')
    # 下載資料
    try:
        data = yf.download(symbol, start=start, end=end)
        cursor = conn.cursor()
        # 檢查資料表是否已經存在日期資料
        for index, row in data.iterrows():
            date_str = index.strftime('%Y-%m-%d')
            
            # 檢查該日期是否已存在於資料庫中
            cursor.execute("SELECT 1 FROM NewTable WHERE Date = ? AND Tickers = ?", (date_str, symbol))
            result = cursor.fetchone()
            
            if result is None:  # 如果該日期不存在，則插入資料
                open_price = row['Open'].iloc[0] if pd.notnull(row['Open'].iloc[0]) else None
                high = row['High'].iloc[0] if pd.notnull(row['High'].iloc[0]) else None
                low = row['Low'].iloc[0] if pd.notnull(row['Low'].iloc[0]) else None
                adj_close = row['Adj Close'].iloc[0] if pd.notnull(row['Adj Close'].iloc[0]) else None
                volume = row['Volume'].iloc[0] if pd.notnull(row['Volume'].iloc[0]) else None
                close = row['Close'].iloc[0] if pd.notnull(row['Close'].iloc[0]) else None

                
                # 插入資料
                insertSQL = """
                    INSERT OR IGNORE INTO NewTable (Date, "Open", High, Low, "Adj Close", Volume, "Close", Tickers)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
                cursor.execute(insertSQL, (date_str, open_price, high, low, adj_close, volume, close, symbol))
        conn.commit()
        messagebox.showinfo('下載狀態','下載完成')
    except Exception as e:
        print(f'Error occurred: {e}')
    finally:
        # 確保連接被關閉
        if conn:
            # 提交更改並關閉連接
            cursor.close()
            conn.close()

