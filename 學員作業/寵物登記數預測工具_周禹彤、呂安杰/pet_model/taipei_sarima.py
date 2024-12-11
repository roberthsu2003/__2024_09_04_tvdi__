import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 設定中文字型
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 可調參數
PARAMS = {
    'train_size': 0.7,
    'order': (1, 1, 1),
    'seasonal_order': (1, 1, 1, 12),
    'enforce_stationarity': False,
    'enforce_invertibility': False
}

def prepare_data():
    try:
        # 嘗試不同的編碼方式
        encodings = ['utf-8', 'big5', 'cp950', 'gb18030']
        taipei_df = None
        budget_df = None
        
        for encoding in encodings:
            try:
                taipei_df = pd.read_csv('processed_taipei_pet_data.csv', encoding=encoding)
                budget_df = pd.read_csv('絕育補助預算表.csv', encoding=encoding)
                print(f"成功使用 {encoding} 編碼讀取檔案")
                break
            except UnicodeDecodeError:
                continue
            
        if taipei_df is None or budget_df is None:
            raise Exception("無法以任何編碼方式讀取檔案")
        
        # 處理預算數據
        budget_df['預算'] = budget_df['台北市預算'].str.replace(',', '').astype(float)
        
        # 轉換日期並設置為索引
        taipei_df['date'] = pd.to_datetime(taipei_df['年'].astype(str) + '-' + 
                                         taipei_df['月'].astype(str) + '-01')
        taipei_df.set_index('date', inplace=True)
        taipei_df = taipei_df.sort_index()
        
        return taipei_df, budget_df
        
    except Exception as e:
        print(f"讀取檔案時發生錯誤: {str(e)}")
        raise

def train_and_predict(data):
    # 確保數據是按時間排序的
    data = data.sort_index()
    
    # 分割訓練集和測試集
    split_idx = int(len(data) * PARAMS['train_size'])
    train_data = data.iloc[:split_idx]
    test_data = data.iloc[split_idx:]
    
    print(f"訓練集大小: {len(train_data)}")
    print(f"測試集大小: {len(test_data)}")
    
    # 訓練SARIMA模型
    model = SARIMAX(train_data['登記數'],
                    order=PARAMS['order'],
                    seasonal_order=PARAMS['seasonal_order'],
                    enforce_stationarity=PARAMS['enforce_stationarity'],
                    enforce_invertibility=PARAMS['enforce_invertibility'])
    
    results = model.fit()
    
    # 對整個歷史期間進行預測
    historical_pred = results.get_prediction(start=data.index[0], end=data.index[-1])
    historical_mean = historical_pred.predicted_mean
    
    # 預測2024年11月到2025年12月的數據
    forecast_dates = pd.date_range(start='2024-12-01', end='2025-12-31', freq='ME')
    forecast = results.get_forecast(steps=len(forecast_dates))
    forecast_mean = forecast.predicted_mean
    
    # 確保預測值的索引正確
    forecast_mean.index = forecast_dates
    
    # 計算測試集的準確度指標
    test_predictions = historical_mean[test_data.index]
    mape = mean_absolute_percentage_error(test_data['登記數'], test_predictions)
    rmse = np.sqrt(mean_squared_error(test_data['登記數'], test_predictions))
    
    # 獲取最後一個實際值的日期
    last_actual_date = data.index[-1]
    
    return historical_mean, forecast_mean, mape, rmse, last_actual_date

def plot_results(data, historical_pred, future_pred, last_actual_date):
    plt.figure(figsize=(15, 7))
    
    # 繪製實際值
    plt.plot(data.index, data['登記數'], 
            label='實際值', color='blue', linewidth=2)
    
    # 繪製歷史預測值（到最後一個實際值）
    plt.plot(historical_pred.loc[:last_actual_date].index, 
            historical_pred.loc[:last_actual_date], 
            label='預測值', color='orange', linewidth=2)
    
    # 繪製未來預測值（包括最後一個實際值，以確保連續性）
    full_pred = pd.concat([
        historical_pred[last_actual_date:last_actual_date],  # 包含最後一個實際值的預測
        future_pred
    ])
    plt.plot(full_pred.index, full_pred, 
            color='orange', linewidth=2)
    
    # 設置標題和標籤
    plt.title('台北市寵物登記數預測結果 (2015-2025)', fontsize=14, pad=15)
    plt.xlabel('年份', fontsize=12)
    plt.ylabel('寵物登記數', fontsize=12)
    
    # 設置圖例
    plt.legend(prop={'size': 12}, loc='upper left')
    
    # 添加網格
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # 設置x軸刻度
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gcf().autofmt_xdate()
    
    # 設置y軸數值格式（千分位）
    plt.gca().yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, p: format(int(x), ','))
    )
    
    # 調整邊距
    plt.tight_layout()
    plt.show()

def main():
    print("開始分析台北市寵物登記數據...")
    
    try:
        # 準備數據
        taipei_df, _ = prepare_data()
        
        # 訓練模型並進行預測
        print("\n訓練模型並進行預測...")
        historical_pred, future_pred, mape, rmse, last_actual_date = train_and_predict(taipei_df)
        
        # 顯示模型性能
        print("\n模型性能指標：")
        print(f"MAPE (平均絕對百分比誤差): {mape:.2%}")
        print(f"RMSE (均方根誤差): {rmse:.2f}")
        print(f"平均每月預測誤差範圍: ±{rmse:.0f}個登記數")
        
        # 顯示未來預測結果
        print("\n未來預測結果：")
        for date, pred in future_pred.items():
            print(f"{date.strftime('%Y年%m月')}預測登記數: {int(pred):,}")
        
        # 繪製結果圖表
        print("\n繪製預測結果圖表...")
        plot_results(taipei_df, historical_pred, future_pred, last_actual_date)
        
    except Exception as e:
        print(f"執行過程中發生錯誤: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main()