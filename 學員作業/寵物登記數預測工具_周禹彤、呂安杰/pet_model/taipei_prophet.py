import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.linear_model import LinearRegression

def setup_chinese_font():
    """設置中文字體"""
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial Unicode MS', 'SimHei']
    plt.rcParams['axes.unicode_minus'] = False

def load_and_preprocess_data(filepath):
    """讀取和預處理數據"""
    df = pd.read_csv(filepath)
    df['ds'] = pd.to_datetime(df.apply(lambda x: f"{int(x['年'])}-{int(x['月']):02d}-01", axis=1))
    df['y'] = df['登記數']
    df = df.sort_values('ds')
    df['month'] = df['ds'].dt.month
    df['year'] = df['ds'].dt.year
    return df

def create_features(df):
    """創建特徵"""
    # 計算移動平均特徵
    df['MA3'] = df['y'].rolling(window=3, min_periods=1).mean()
    df['MA6'] = df['y'].rolling(window=6, min_periods=1).mean()
    
    # 絕育相關特徵
    df['neuter_MA3'] = df['絕育數'].rolling(window=3, min_periods=1).mean()
    df['neuter_rate_MA3'] = df['絕育率'].rolling(window=3, min_periods=1).mean()
    
    # 計算月度季節性
    monthly_avg = df.groupby('month')['y'].transform('mean')
    df['month_avg'] = monthly_avg / monthly_avg.mean()
    
    return df

def scale_features(df, features_to_scale):
    """特徵標準化"""
    scaled_features = {}
    for col in features_to_scale:
        mean = df[col].mean()
        std = df[col].std()
        df[f'{col}_scaled'] = (df[col] - mean) / std
        scaled_features[col] = {'mean': mean, 'std': std}
    return df, scaled_features

def analyze_feature_importance(df, features, target='y'):
    """分析特徵重要性"""
    # 相關性分析
    correlations = df[features].corrwith(df[target])
    
    # 線性回歸係數分析
    reg = LinearRegression()
    X = df[features]
    y = df[target]
    reg.fit(X, y)
    
    # 合併結果
    importance_df = pd.DataFrame({
        '特徵名稱': features,
        '相關係數': correlations.values,
        '回歸係數': reg.coef_,
        '絕對回歸係數': np.abs(reg.coef_)
    })
    
    # 排序結果
    importance_df = importance_df.sort_values('絕對回歸係數', ascending=False)
    
    return importance_df

def train_prophet_model(train_df, selected_features):
    """訓練Prophet模型"""
    model = Prophet(
        changepoint_prior_scale=0.001,
        seasonality_prior_scale=1.0,
        holidays_prior_scale=0.01,
        seasonality_mode='additive',
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False,
        changepoint_range=0.8
    )
    
    # 添加月度季節性
    model.add_seasonality(
        name='monthly',
        period=30.5,
        fourier_order=3
    )
    
    # 添加特徵
    for feature in selected_features:
        model.add_regressor(feature)
    
    # 訓練模型
    train_prophet = train_df[['ds', 'y'] + selected_features].copy()
    model.fit(train_prophet)
    
    return model

def main():
    # 設置中文字體
    setup_chinese_font()
    
    # 讀取數據
    df = load_and_preprocess_data('processed_taipei_pet_data.csv')
    
    # 創建特徵
    df = create_features(df)
    
    # 特徵列表
    features_to_scale = ['MA3', 'MA6', 'month_avg', 'neuter_MA3', 'neuter_rate_MA3']
    
    # 特徵標準化
    df, scaled_features = scale_features(df, features_to_scale)
    selected_features = [f'{col}_scaled' for col in features_to_scale]
    
    # 分析特徵重要性
    importance_df = analyze_feature_importance(df, features_to_scale)
    
    # 分割訓練集和測試集（70/30）
    train_size = int(len(df) * 0.7)
    train_df = df[:train_size]
    test_df = df[train_size:]
    
    # 訓練模型
    model = train_prophet_model(train_df, selected_features)
    
    # 預測
    test_forecast = model.predict(test_df[['ds'] + selected_features])
    historical_forecast = model.predict(df[['ds'] + selected_features])
    
    # 準備未來預測
    future_dates = pd.DataFrame({
        'ds': pd.date_range(start='2024-12-01', end='2025-12-31', freq='MS')
    })
    for feature in selected_features:
        future_dates[feature] = df[feature].iloc[-1]
    
    future_forecast = model.predict(future_dates)
    all_forecast = pd.concat([historical_forecast, future_forecast])
    
    # 計算評估指標
    y_true = test_df['y'].values
    y_pred = test_forecast['yhat'].values
    
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    r2 = r2_score(y_true, y_pred)
    mean_error = np.mean(np.abs(y_true - y_pred))
    
    # 輸出結果
    print("\n特徵重要性分析:")
    print(importance_df.to_string(index=False))
    
    print(f"\n模型評估指標:")
    print(f"RMSE: {rmse:.2f}")
    print(f"MAPE: {mape:.2f}%")
    print(f"R平方: {r2:.4f}")
    print(f"平均每月預測誤差範圍: ±{mean_error:.2f}")
    
    print("\n2024年12月~2025年12月預測值:")
    future_predictions = future_forecast[['ds', 'yhat']]
    for _, row in future_predictions.iterrows():
        print(f"{row['ds'].strftime('%Y年%m月')}: {int(row['yhat'])}")
    
    # 繪製圖表
    plt.figure(figsize=(15, 7))
    plt.plot(df['ds'], df['y'], label='實際值', color='blue', linewidth=2)
    plt.plot(all_forecast['ds'], all_forecast['yhat'], label='預測值', color='orange', linewidth=2)
    
    plt.title('台北市寵物登記數預測結果 (2015-2025)', fontsize=14, pad=15)
    plt.xlabel('年份', fontsize=12)
    plt.ylabel('登記數量', fontsize=12)
    plt.legend(prop={'size': 12}, loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gcf().autofmt_xdate()
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()