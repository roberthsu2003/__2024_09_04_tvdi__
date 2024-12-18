import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy import stats

# 設定中文字型
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 進一步優化的參數
PARAMS = {
    'train_size': 0.7,
    'xgb_params': {
        'n_estimators': 50,         # 樹的數量
        'learning_rate': 0.03,      # 提高學習率以增加波動
        'max_depth': 4,             # 增加深度以捕捉更多模式
        'min_child_weight': 3,      # 降低以增加彈性
        'subsample': 0.8,           # 提高採樣比例
        'colsample_bytree': 0.8,    # 提高特徵採樣比例
        'reg_alpha': 0.3,           # 降低L1正則化以增加波動
        'reg_lambda': 1,            # 降低L2正則化以增加波動
        'random_state': 42,
        'objective': 'reg:squarederror'
    }
}

def generate_future_dates():
    """生成未來日期序列"""
    return pd.date_range(start='2024-12-01', end='2025-12-31', freq='M')

def prepare_future_features(data, future_dates, model, scaler, features):
    """準備未來預測所需的特徵
    
    參數:
        data: 歷史數據
        future_dates: 未來日期序列
        model: 訓練好的模型
        scaler: 特徵縮放器
        features: 特徵列表
    """
    future_data = pd.DataFrame(index=future_dates)
    future_data['month'] = future_data.index.month
    future_data['month_sin'] = np.sin(2 * np.pi * future_data['month']/12)
    future_data['month_cos'] = np.cos(2 * np.pi * future_data['month']/12)
    future_data['season'] = future_data['month'].apply(lambda x: (x%12 + 3)//3)
    
    # 使用最近12個月的平均值
    recent_data = data.tail(12)
    future_data['monthly_budget'] = recent_data['monthly_budget'].iloc[-1]
    future_data['絕育數'] = recent_data['絕育數'].mean()
    future_data['絕育率'] = recent_data['絕育率'].mean()
    
    # 動態計算滾動特徵和lag特徵
    all_predictions = []
    for i in range(len(future_data)):
        if i == 0:
            # 第一個月使用歷史數據的最後值
            future_data.loc[future_dates[i], 'reg_lag_1'] = data['登記數'].iloc[-1]
            future_data.loc[future_dates[i], 'reg_lag_2'] = data['登記數'].iloc[-2]
            future_data.loc[future_dates[i], 'neut_lag_1'] = data['絕育數'].iloc[-1]
            
            recent_values = list(data['登記數'].tail(6))
            future_data.loc[future_dates[i], 'rolling_mean_3m'] = np.mean(recent_values[-3:])
            future_data.loc[future_dates[i], 'rolling_mean_6m'] = np.mean(recent_values)
            future_data.loc[future_dates[i], 'rolling_std_3m'] = np.std(recent_values[-3:])
            future_data.loc[future_dates[i], 'neut_reg_ratio'] = data['neut_reg_ratio'].iloc[-1]
        else:
            # 後續月份使用預測值
            future_data.loc[future_dates[i], 'reg_lag_1'] = all_predictions[i-1]
            future_data.loc[future_dates[i], 'reg_lag_2'] = all_predictions[i-2] if i > 1 else data['登記數'].iloc[-1]
            future_data.loc[future_dates[i], 'neut_lag_1'] = future_data['絕育數'].iloc[i-1]
            
            recent_pred = all_predictions[-3:] if len(all_predictions) >= 3 else data['登記數'].tail(3).tolist()
            future_data.loc[future_dates[i], 'rolling_mean_3m'] = np.mean(recent_pred)
            future_data.loc[future_dates[i], 'rolling_mean_6m'] = np.mean(recent_pred)
            future_data.loc[future_dates[i], 'rolling_std_3m'] = np.std(recent_pred)
            future_data.loc[future_dates[i], 'neut_reg_ratio'] = future_data['絕育數'].iloc[i] / np.mean(recent_pred)
        
        # 進行預測
        temp_pred = model.predict(scaler.transform(future_data.loc[[future_dates[i]], features]))
        all_predictions.append(float(temp_pred[0]))
    
    return future_data, all_predictions

def prepare_data():
    try:
        # 讀取數據
        xinpei_df = pd.read_csv('processed_xinpei_pet_data.csv', encoding='utf-8')
        budget_df = pd.read_csv('絕育補助預算表.csv', encoding='utf-8')
        
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
        
        # 基本時間特徵
        merged_data['month'] = merged_data['date'].dt.month
        merged_data['year'] = merged_data['date'].dt.year
        merged_data['season'] = merged_data['month'].apply(lambda x: (x%12 + 3)//3)
        merged_data['month_sin'] = np.sin(2 * np.pi * merged_data['month']/12)
        merged_data['month_cos'] = np.cos(2 * np.pi * merged_data['month']/12)
        
        # 優化滾動特徵
        merged_data['rolling_mean_3m'] = merged_data['登記數'].rolling(window=3, min_periods=1).mean()
        merged_data['rolling_mean_6m'] = merged_data['登記數'].rolling(window=6, min_periods=1).mean()
        merged_data['rolling_std_3m'] = merged_data['登記數'].rolling(window=3, min_periods=1).std()
        
        # 優化lag特徵
        for i in [1, 2, 3]:
            merged_data[f'reg_lag_{i}'] = merged_data['登記數'].shift(i)
            merged_data[f'neut_lag_{i}'] = merged_data['絕育數'].shift(i)
        
        # 比率特徵
        merged_data['neut_reg_ratio'] = merged_data['絕育數'] / merged_data['登記數']
        
        # 移除極端值 (使用更保守的閾值)
        for col in ['登記數', '絕育數', '絕育率']:
            q1 = merged_data[col].quantile(0.1)
            q3 = merged_data[col].quantile(0.9)
            iqr = q3 - q1
            lower_bound = q1 - 1.0 * iqr  # 使用更保守的倍數
            upper_bound = q3 + 1.0 * iqr
            merged_data[col] = merged_data[col].clip(lower_bound, upper_bound)
        
        # 移除缺失值
        merged_data = merged_data.dropna()
        
        print(f"資料處理完成，共有 {len(merged_data)} 筆資料")
        return merged_data
        
    except Exception as e:
        print(f"讀取檔案時發生錯誤: {str(e)}")
        raise

def train_model(data):
    # 準備特徵 (減少特徵數量，保留最重要的特徵)
    features = [
        'month_sin', 'month_cos', 'season',
        'monthly_budget', '絕育數', '絕育率',
        'rolling_mean_3m', 'rolling_mean_6m', 'rolling_std_3m',
        'reg_lag_1', 'reg_lag_2', 'neut_lag_1',
        'neut_reg_ratio'
    ]
    
    X = data[features]
    y = data['登記數']
    
    # 分割數據 (使用 train_test_split 來確保隨機性)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        train_size=PARAMS['train_size'], 
        random_state=42
    )
    
    # 使用 RobustScaler 來處理異常值
    scaler = RobustScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 訓練模型
    model = xgb.XGBRegressor(**PARAMS['xgb_params'])
    model.fit(X_train_scaled, y_train)
    
    # 預測
    X_all_scaled = scaler.transform(X)
    all_predictions = model.predict(X_all_scaled)
    test_predictions = model.predict(X_test_scaled)
    
    # 計算評估指標
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

def plot_results(data, predictions, future_dates, future_predictions):
    """繪製預測結果圖表
    
    參數:
        data: 歷史數據
        predictions: 歷史預測值
        future_dates: 未來日期序列
        future_predictions: 未來預測值
    """
    plt.figure(figsize=(15, 7))
    
    # 繪製實際值（2015年1月至2024年11月）
    actual_mask = (data['date'] >= '2015-01-01') & (data['date'] <= '2024-11-30')
    plt.plot(data.loc[actual_mask, 'date'], 
            data.loc[actual_mask, '登記數'], 
            label='實際值', 
            color='blue', 
            linewidth=2)
    
    # 繪製預測值（包含歷史預測和未來預測）
    # 1. 準備歷史預測數據
    historical_dates = data.loc[actual_mask, 'date']
    historical_predictions = predictions[actual_mask]
    
    # 2. 準備未來預測數據（包含最後一個歷史點以確保連續性）
    all_prediction_dates = pd.concat([
        pd.Series(historical_dates),
        pd.Series(future_dates)
    ])
    
    all_prediction_values = np.concatenate([
        historical_predictions,
        future_predictions
    ])
    
    # 3. 繪製完整的預測線（使用實線）
    plt.plot(all_prediction_dates, 
            all_prediction_values,
            label='預測值',
            color='orange',
            linewidth=2)
    
    # 設置圖表標題和標籤
    plt.title('新北市寵物登記數預測結果 (2015-2025)', fontsize=14, pad=15)
    plt.xlabel('年份', fontsize=12)
    plt.ylabel('寵物登記數', fontsize=12)
    
    # 設置圖例
    plt.legend(prop={'size': 12}, loc='upper left')
    
    # 添加網格
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # 設置x軸格式
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

# 主程式和其他函數保持不變

def main():
    print("開始分析新北市寵物登記數據...")
    
    try:
        # 準備數據
        data = prepare_data()
        
        # 訓練模型
        print("\n開始訓練模型...")
        model, scaler, predictions, actual_values, metrics, features = train_model(data)
        
        # 生成未來日期
        future_dates = generate_future_dates()
        
        # 準備未來預測數據並進行預測（加入model和scaler參數）
        future_data, future_predictions = prepare_future_features(
            data, future_dates, model, scaler, features
        )
        
        # 顯示模型性能
        print("\n模型性能指標：")
        print(f"MAPE (平均絕對百分比誤差): {metrics['mape']:.2%}")
        print(f"RMSE (均方根誤差): {metrics['rmse']:.2f}")
        print(f"MAE (平均絕對誤差): {metrics['mae']:.2f}")
        print(f"R² (決定係數): {metrics['r2']:.4f}")
        
        # 繪製結果圖表
        plot_results(data, predictions, future_dates, future_predictions)
        
        # 顯示特徵重要性
        feature_importance = pd.DataFrame({
            'feature': features,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\n特徵重要性：")
        print(feature_importance)
        
        # 顯示未來預測結果
        print("\n2025年預測結果：")
        for date, pred in zip(future_dates, future_predictions):
            print(f"{date.strftime('%Y年%m月')}預測登記數: {int(pred):,}")
            
    except Exception as e:
        print(f"執行過程中發生錯誤: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main()