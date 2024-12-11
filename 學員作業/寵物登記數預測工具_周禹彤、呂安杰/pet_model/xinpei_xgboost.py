import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy import stats

# 設定中文字型
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 優化後的參數
PARAMS = {
    'train_size': 0.7,
    'xgb_params': {
        'n_estimators': 200,
        'learning_rate': 0.1,
        'max_depth': 6,
        'min_child_weight': 2,
        'subsample': 0.7,
        'colsample_bytree': 0.7,
        'random_state': 42
    }
}

def detect_outliers(df, column, z_threshold=3):
    """檢測異常值"""
    z_scores = np.abs(stats.zscore(df[column]))
    return z_scores > z_threshold

def prepare_data():
    try:
        # 嘗試不同的編碼方式
        encodings = ['utf-8', 'big5', 'cp950', 'gb18030']
        xinpei_df = None
        budget_df = None
        
        for encoding in encodings:
            try:
                xinpei_df = pd.read_csv('processed_xinpei_pet_data.csv', encoding=encoding)
                budget_df = pd.read_csv('絕育補助預算表.csv', encoding=encoding)
                print(f"成功使用 {encoding} 編碼讀取檔案")
                break
            except UnicodeDecodeError:
                continue
            
        if xinpei_df is None or budget_df is None:
            raise Exception("無法以任何編碼方式讀取檔案")

        # 處理預算數據
        budget_df['預算'] = budget_df['新北市預算'].str.replace(',', '').astype(float)
        budget_df['monthly_budget'] = budget_df['預算'] / 12
        
        # 確保年份型態一致
        budget_df['年'] = budget_df['西元年分'].astype(str)
        xinpei_df['年'] = xinpei_df['年'].astype(str)
        
        # 轉換日期並創建特徵
        xinpei_df['date'] = pd.to_datetime(xinpei_df['年'].astype(str) + '-' + 
                                         xinpei_df['月'].astype(str) + '-01')
        
        # 合併數據
        merged_data = pd.merge(xinpei_df, budget_df[['年', 'monthly_budget']], on='年')
        
        # 依日期排序
        merged_data = merged_data.sort_values('date')
        
        # 創建基本特徵
        merged_data['month'] = merged_data['date'].dt.month
        merged_data['year'] = merged_data['date'].dt.year
        merged_data['previous_month_registrations'] = merged_data['登記數'].shift(1)
        merged_data['previous_month_neutering'] = merged_data['絕育數'].shift(1)
        
        # 添加新特徵
        merged_data['season'] = merged_data['month'].apply(lambda x: (x%12 + 3)//3)
        merged_data['month_sin'] = np.sin(2 * np.pi * merged_data['month']/12)
        merged_data['month_cos'] = np.cos(2 * np.pi * merged_data['month']/12)
        merged_data['rolling_mean_3m'] = merged_data['登記數'].rolling(window=3, min_periods=1).mean()
        merged_data['rolling_std_3m'] = merged_data['登記數'].rolling(window=3, min_periods=1).std()
        
        # 檢測並處理異常值
        outliers = detect_outliers(merged_data, '登記數')
        merged_data.loc[outliers, '登記數'] = merged_data['rolling_mean_3m']
        
        # 移除缺失值
        merged_data = merged_data.dropna()
        
        print(f"資料處理完成，共有 {len(merged_data)} 筆資料")
        return merged_data
        
    except Exception as e:
        print(f"讀取檔案時發生錯誤: {str(e)}")
        raise

def train_model(data):
    # 準備特徵
    features = ['month', 'month_sin', 'month_cos', 'season',
                'monthly_budget', '絕育數', '絕育率',
                'previous_month_registrations', 'previous_month_neutering',
                'rolling_mean_3m', 'rolling_std_3m']
    X = data[features]
    y = data['登記數']
    
    # 分割數據
    split_idx = int(len(data) * PARAMS['train_size'])
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    # 標準化特徵
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 訓練模型
    model = xgb.XGBRegressor(**PARAMS['xgb_params'])
    model.fit(X_train_scaled, y_train)
    
    # 預測整個時期的數據
    X_all_scaled = scaler.transform(X)
    all_predictions = model.predict(X_all_scaled)
    
    # 計算各種評估指標
    test_predictions = model.predict(X_test_scaled)
    mape = mean_absolute_percentage_error(y_test, test_predictions)
    rmse = np.sqrt(mean_squared_error(y_test, test_predictions))
    mae = mean_absolute_error(y_test, test_predictions)
    r2 = r2_score(y_test, test_predictions)
    
    metrics = {
        'mape': mape,
        'rmse': rmse,
        'mae': mae,
        'r2': r2
    }
    
    return model, scaler, all_predictions, data['登記數'].values, metrics, features

def calculate_seasonal_factors(data):
    """計算季節性因子"""
    seasonal_factors = data.groupby('month')['登記數'].mean() / data['登記數'].mean()
    return seasonal_factors

def predict_future(model, scaler, last_data, features):
    # 獲取季節性因子
    seasonal_factors = calculate_seasonal_factors(last_data)
    
    # 準備2024年12月到2025年12月的預測數據
    future_months = pd.date_range(start='2024-12-01', end='2025-12-31', freq='ME')
    future_data = pd.DataFrame()
    
    # 初始化預測資料框
    future_data['month'] = [d.month for d in future_months]
    future_data['month_sin'] = np.sin(2 * np.pi * future_data['month']/12)
    future_data['month_cos'] = np.cos(2 * np.pi * future_data['month']/12)
    future_data['season'] = future_data['month'].apply(lambda x: (x%12 + 3)//3)
    
    # 使用最近的數據
    last_12_months = last_data.tail(12)
    future_data['monthly_budget'] = last_data['monthly_budget'].iloc[-1]
    future_data['絕育數'] = last_12_months['絕育數'].mean()
    future_data['絕育率'] = last_12_months['絕育率'].mean()
    future_data['previous_month_registrations'] = last_12_months['登記數'].mean()
    future_data['previous_month_neutering'] = last_12_months['絕育數'].mean()
    future_data['rolling_mean_3m'] = last_12_months['rolling_mean_3m'].mean()
    future_data['rolling_std_3m'] = last_12_months['rolling_std_3m'].mean()
    
    # 進行動態預測
    predictions = []
    for i in range(len(future_months)):
        if i > 0:
            future_data.loc[i, 'previous_month_registrations'] = predictions[-1]
        
        # 標準化當前月份的特徵
        current_features = future_data.iloc[[i]][features]
        current_scaled = scaler.transform(current_features)
        
        # 預測並應用季節性調整
        pred = model.predict(current_scaled)[0]
        pred *= seasonal_factors[future_data.iloc[i]['month']]
        predictions.append(pred)
    
    return np.array(predictions), future_months

def plot_results(actual_dates, actual_values, historical_pred, future_dates, future_pred):
    plt.figure(figsize=(15, 7))
    
    # 確保所有數據長度一致
    n = len(actual_values)
    actual_dates = actual_dates[:n]
    historical_pred = historical_pred[:n]
    
    # 繪製實際值
    plt.plot(actual_dates, actual_values, 
            label='實際值', color='blue', linewidth=2)
    
    # 繪製歷史預測值
    plt.plot(actual_dates, historical_pred, 
            label='預測值', color='orange', linewidth=2)
    
    # 繪製未來預測值（確保連續性）
    all_pred_dates = pd.concat([pd.Series(actual_dates[-1:]), pd.Series(future_dates)])
    all_pred_values = np.concatenate([historical_pred[-1:], future_pred])
    plt.plot(all_pred_dates, all_pred_values, 
            color='orange', linewidth=2)
    
    # 設置標題和標籤
    plt.title('新北市寵物登記數預測結果 (2015-2025)', fontsize=14, pad=15)
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
    print("開始分析新北市寵物登記數據...")
    
    try:
        # 準備數據
        data = prepare_data()
        
        # 生成實際日期範圍
        actual_dates = data['date'].values
        
        # 訓練模型
        print("\n開始訓練模型...")
        model, scaler, historical_pred, actual_values, metrics, features = train_model(data)
        
        # 顯示模型性能
        print("\n模型性能指標：")
        print(f"MAPE (平均絕對百分比誤差): {metrics['mape']:.2%}")
        print(f"RMSE (均方根誤差): {metrics['rmse']:.2f}")
        print(f"MAE (平均絕對誤差): {metrics['mae']:.2f}")
        print(f"R² (決定係數): {metrics['r2']:.4f}")
        print(f"平均每月預測誤差範圍: ±{metrics['rmse']:.0f}個登記數")
        
        # 預測未來數據
        print("\n進行未來預測...")
        future_pred, future_dates = predict_future(model, scaler, data, features)
        
        print("\n2025年預測結果：")
        for date, pred in zip(future_dates, future_pred):
            print(f"{date.strftime('%Y年%m月')}預測登記數: {int(pred):,}")
        
        # 繪製結果圖表
        print("\n繪製預測結果圖表...")
        plot_results(actual_dates, actual_values, historical_pred, future_dates, future_pred)
        
        # 顯示特徵重要性
        feature_importance = pd.DataFrame({
            'feature': features,
            'importance': model.feature_importances_
        })
        print("\n特徵重要性：")
        print(feature_importance.sort_values('importance', ascending=False))
        
    except Exception as e:
        print(f"執行過程中發生錯誤: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main()