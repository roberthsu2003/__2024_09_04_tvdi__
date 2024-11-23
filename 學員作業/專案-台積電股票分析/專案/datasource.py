import yfinance as yf
import sqlite3
import pandas as pd
from datetime import datetime, timedelta 
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import pandas_datareader as web
import requests
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import SGDRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from matplotlib import rcParams
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def date(close):
    conn=sqlite3.connect("check_data.db")
    with conn:
        cursor= conn.cursor()
        sql= '''SELECT DISTINCT Close FROM NewTable where Date =?'''

        cursor.execute(sql,(close,))
        date = [items[0] for items in cursor.fetchall()]
    return date

def get_close():
    conn = sqlite3.connect('check_data.db')
    with conn:
        cursor= conn.cursor()
        sql = '''SELECT DISTINCT Close From NewTable'''
        cursor.execute(sql)
        close = [items[0] for items in cursor.fetchall()]
    return close






def download_data():
    print("download_data function is called")
    symbol = '2330.TW'
    start = '2020-01-01'
    end = (dt.datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
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



#calculate

def linear_regression():
    
    
    # 連接到 SQLite 資料庫
    conn = sqlite3.connect('check_data.db')

    # 從資料庫讀取資料
    sql = '''SELECT * FROM NewTable'''
    data_from_db = pd.read_sql(sql, conn)

    # 關閉資料庫連接
    conn.close()
    
    # 將索引轉換為日期格式
    data_from_db['Date'] = pd.to_datetime(data_from_db['Date'])
    # 將日期轉換為從最早日期起的天數
    data_from_db['Days'] = (data_from_db['Date'] - data_from_db['Date'].min()).dt.days

    X = data_from_db.iloc[2:-2].select_dtypes(include=[np.number]).drop(columns=['Close'])  # 僅選擇數值型欄位，排除 'Close' # 自變量，移除前2行和後2行
    y = data_from_db['Close'].iloc[2:-2]  # 目標變量，與 X 範圍一致
    
   
    print(X.dtypes)  # 應該只包含數值型資料
    print("=============")
    print(y.dtypes)  # 應該是數值型

    # 線性回歸模型

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.6, random_state = 0,shuffle=False)
    model = LinearRegression(fit_intercept=True,copy_X=True,n_jobs=1)
    model.fit(X_train, y_train)
    model_score = model.score(X_train, y_train)
    b = model.intercept_
    a = model.coef_
    correlations = data_from_db.iloc[2:-2].select_dtypes(include=[np.number]).corr()
    relevant_features = correlations['Close'].sort_values(ascending=False)
    
    print(f'Model Score (R²): {model_score:.4f}\nCoeficient: {a} \nIntercept: {b}')
    print("=========================================")
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test,y_pred)
    r2 = r2_score(y_test,y_pred)
    print(f'Model Score (R²): {r2:.4f}\nMean Squared Error: {mse}')
    print("=========================================")
    print(relevant_features)

    # if not X_test.empty:
    #     try:
    #         test_dates = data_from_db.loc[X_test.index, :].index
    #         print(test_dates[:5])
    #     except Exception as e:
    #         print(f"Error calculating test_dates: {e}")
    # else:
    #     print("X_test is empty, cannot calculate test_dates.")


    # 確保 X_test 是帶有列名稱的 DataFrame
    X_test = pd.DataFrame(X_test, columns=X.columns)
    X_test_sorted = X_test.sort_index()
    # 提取測試集對應的日期
    test_dates = data_from_db.loc[X_test_sorted .index,'Date']
    
    y_test_pred = model.predict(X_test_sorted )
    

    # 繪圖
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data_from_db['Date'], data_from_db['Close'], label='Historical Close Price', color='Blue')

    # 使用 model 預測的值
    # 繪製測試集預測結果
    ax.plot(test_dates, y_test_pred, label='Linear Regression', color='orange')

    #plt.scatter(test_dates, y_test_pred, label='Linear Regression', color='orange')
    
    
    # 進行預測
    # 未來30天
    future_days = 30

    # 獲取最後一個日期的天數
    last_day = data_from_db['Date'].max()
    # 使用模型進行預測
    # 建立 future_x 為帶列名稱的 DataFrame
    future_x = pd.DataFrame(
    np.arange(data_from_db['Days'].max() + 1, data_from_db['Days'].max() + future_days + 1),
    columns=['Days'])
    future_x=future_x.sort_values(by='Days')

    # 填充其他特徵，確保與模型訓練的特徵一致
    for col in ['Open', 'High', 'Low', 'Adj Close', 'Volume', 'Days']:
        diff_mean = data_from_db[col].diff().mean()
        if col == 'Days':
            future_x[col] = np.arange(data_from_db['Days'].max() + 1, data_from_db['Days'].max() + 31)
        else:
            future_x[col] = data_from_db[col].iloc[-1] + (diff_mean if not pd.isna(diff_mean) else 0)
    
    future_x = future_x[X.columns]
    
    #future_x = np.arange(data_from_db['Days'].max() + 1, data_from_db['Days'].max() + future_days + 1).reshape(-1, 1)
    
    future_x_sorted=future_x.sort_values(by='Days')
    predicted_price = model.predict(future_x_sorted)

    # 將預測結果轉換為日期格式，從最後一天開始
    future_dates = [last_day + pd.Timedelta(days=i) for i in range(1, future_days + 1)]

    # 顯示預測價格
    ax.plot(future_dates, predicted_price, label='Future Prediction', color='red', linestyle='--')

    ax.set_xlim(data_from_db['Date'].min(), future_dates[-1])
    ax.set_ylim(data_from_db['Close'].min() - 10, data_from_db['Close'].max() + 10)
    ax.set_xlabel('Date')
    ax.set_ylabel('Close Price')
    ax.set_title('Close Price and Linear Regression Line with Prediction')
    ax.legend()
    
    return fig



def rsi():
    # 連接到 SQLite 資料庫
    conn = sqlite3.connect('check_data.db')

    # 從資料庫讀取資料
    sql = '''SELECT * FROM NewTable'''
    data_from_db = pd.read_sql(sql, conn)

    # 關閉資料庫連接
    conn.close()

    data_from_db['Date'] = pd.to_datetime(data_from_db['Date'])
    # 將日期轉換為從最早日期起的天數
    data_from_db['Days'] = (data_from_db['Date'] - data_from_db['Date'].min()).dt.days

    
    rcParams['font.family'] = 'Microsoft JhengHei'  # 微軟正黑體（或替換為系統中的其他中文字體）
    # Step 2: 計算 RSI
    window = 14  # RSI 計算窗口

    # 計算每日價格變化
    delta = data_from_db['Close'].diff()

    # 分別計算上漲和下跌數據
    gain = delta.where(delta > 0, 0)  # 上漲數據
    loss = -delta.where(delta < 0, 0)  # 下跌數據

    # 計算平均上漲與平均下跌
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    # 計算 RS 和 RSI
    rs = avg_gain / avg_loss
    data_from_db['RSI'] = 100 - (100 / (1 + rs))

    # Step 3: 繪製圖形
    fig, axes = plt.subplots(2, 1, figsize=(8, 4))

    # 設定背景顏色為灰色
    axes[0].set_facecolor('lightgrey')
    axes[1].set_facecolor('lightgrey')

    # 繪製收盤價
    axes[0].plot(data_from_db['Days'],data_from_db['Close'], label='Close Price', color='blue')
    axes[0].set_title('台積電收盤價', fontsize=14)
    axes[0].set_xlabel('日期', fontsize=10)  # X 軸標籤
    axes[0].set_ylabel('價格 (TWD)', fontsize=10)  # Y 軸標籤
    axes[0].legend()

    # 設置 X 軸的範圍和標籤
    axes[0].set_xlim(data_from_db['Days'].min(), data_from_db['Days'].max())
    axes[0].set_xticks(data_from_db['Days'][::180])  # 每隔 30 天顯示一個標籤
    axes[0].set_xticklabels(data_from_db['Date'][::180].dt.strftime('%Y-%m-%d'))  # 日期格式化
    axes[0].legend()

    # 繪製 RSI
    axes[1].plot(data_from_db['Days'],data_from_db['RSI'], label='RSI', color='purple')
    axes[1].axhline(70, color='red', linestyle='--',
                    linewidth=0.5, label='超買區 (70)')  # 超買區
    axes[1].axhline(30, color='green', linestyle='--',
                    linewidth=0.5, label='超賣區 (30)')  # 超賣區
    axes[1].set_title('RSI 指標', fontsize=10)
    axes[1].set_xlabel('日期', fontsize=10)  # X 軸標籤
    axes[1].set_ylabel('RSI 值', fontsize=10)  # Y 軸標籤
    axes[1].legend()

    # 設置 X 軸的範圍和標籤
    axes[1].set_xlim(data_from_db['Days'].min(), data_from_db['Days'].max())
    axes[1].set_xticks(data_from_db['Days'][::180])  # 每隔 30 天顯示一個標籤
    axes[1].set_xticklabels(data_from_db['Date'][::180].dt.strftime('%Y-%m-%d'))  # 日期格式化
    axes[1].legend()




    # 調整佈局避免重疊
    plt.tight_layout()

    # 顯示圖形
    plt.show()



def sma():
    # 連接到 SQLite 資料庫
    conn = sqlite3.connect('check_data.db')

    # 從資料庫讀取資料
    sql = '''SELECT * FROM NewTable'''
    data_from_db = pd.read_sql(sql, conn)

    # 關閉資料庫連接
    conn.close()

    rcParams['font.family'] = 'Microsoft JhengHei'  # 微軟正黑體（或替換為系統中的其他中文字體）

    data_from_db['Date'] = pd.to_datetime(data_from_db['Date'])
    data_from_db = data_from_db.sort_values(by='Date').reset_index(drop=True)
    # 將日期轉換為從最早日期起的天數
    data_from_db['Days'] = (data_from_db['Date'] - data_from_db['Date'].min()).dt.days
    
    short_window = 20
    long_window = 60

    data_from_db['SMA_short'] = data_from_db['Close'].rolling(window=short_window).mean()
    data_from_db['SMA_long'] = data_from_db['Close'].rolling(window=long_window).mean()

    # 繪製移動平均線與收盤價
    plt.figure(figsize=(14, 7))
    plt.plot(data_from_db['Days'],data_from_db['Close'], label='Close Price', color='blue')
    plt.plot(data_from_db['Days'],data_from_db['SMA_short'], label='20-Day SMA', color='orange', linestyle='--')
    plt.plot(data_from_db['Days'],data_from_db['SMA_long'], label='90-Day SMA', color='grey', linestyle='--')

    # # 標註買入與賣出信號
    # buy_signals = (data_from_db['SMA_short'] > data_from_db['SMA_long']) & (data_from_db['SMA_short'].shift(1) <= data_from_db['SMA_long'].shift(1))
    # sell_signals = (data_from_db['SMA_short'] < data_from_db['SMA_long']) & (data_from_db['SMA_short'].shift(1) >= data_from_db['SMA_long'].shift(1))

    # plt.scatter(data_from_db.loc[buy_signals,'Days'], data_from_db.loc[buy_signals,'Close'], marker='^', color='green', label='Buy Signal', alpha=1)
    # plt.scatter(data_from_db.loc[sell_signals,'Days'], data_from_db.loc[sell_signals,'Close'], marker='v', color='red', label='Sell Signal', alpha=1)

    # 設定買入與賣出信號的條件
    buy_signals = (
        (data_from_db['SMA_short'] > data_from_db['SMA_long']) &
        (data_from_db['SMA_short'].shift(1) <= data_from_db['SMA_long'].shift(1))
    )

    sell_signals = (
        (data_from_db['SMA_short'] < data_from_db['SMA_long']) &
        (data_from_db['SMA_short'].shift(1) >= data_from_db['SMA_long'].shift(1))
    )

    # 繪製買入與賣出信號
    plt.scatter(data_from_db.loc[buy_signals, 'Days'], data_from_db.loc[buy_signals, 'Close'], 
                marker='^', color='green', label='Buy Signal', alpha=1,s=100 )
    plt.scatter(data_from_db.loc[sell_signals, 'Days'], data_from_db.loc[sell_signals, 'Close'], 
                marker='v', color='red', label='Sell Signal', alpha=1,s=100 )


    plt.title('台積電收盤價與移動平均線')
    plt.xlabel('日期')
    plt.ylabel('價格 (TWD)')
    # 設定 x 軸範圍與標籤
    plt.xlim(data_from_db['Days'].min(), data_from_db['Days'].max())
    plt.xticks(
        ticks=data_from_db['Days'][::180],  # 每隔 180 天顯示一個標籤
        labels=data_from_db['Date'][::180].dt.strftime('%Y-%m-%d'),  # 日期格式化
        rotation=45
    )

    plt.legend()
    plt.tight_layout()
    plt.grid()
    plt.show()



