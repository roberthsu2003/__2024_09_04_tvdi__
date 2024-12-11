import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 設定中文字型
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 可調參數
PARAMS = {
    'train_size': 0.7,  # 訓練集比例
    'xgb_params': {
        'n_estimators': 100,     # 樹的數量 - 可調整
        'learning_rate': 0.1,    # 學習率 - 可調整
        'max_depth': 5,          # 樹的最大深度 - 可調整
        'min_child_weight': 1,   # 最小子節點權重 - 可調整
        'subsample': 0.8,        # 樣本採樣比例 - 可調整
        'colsample_bytree': 0.8, # 特徵採樣比例 - 可調整
        'random_state': 42
    }
}

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
        print("處理預算資料...")
        budget_df['預算'] = budget_df['新北市預算'].str.replace(',', '').astype(float)
        budget_df['monthly_budget'] = budget_df['預算'] / 12
        
        # 確保年份型態一致
        print("處理年份資料...")
        budget_df['年'] = budget_df['西元年分'].astype(str)
        xinpei_df['年'] = xinpei_df['年'].astype(str)
        
        # 檢查年份格式
        print("預算資料年份:", budget_df['年'].unique())
        print("登記資料年份:", xinpei_df['年'].unique())
        
        print("處理寵物登記資料...")
        # 轉換日期並創建特徵
        xinpei_df['date'] = pd.to_datetime(xinpei_df['年'].astype(str) + '-' + 
                                          xinpei_df['月'].astype(str) + '-01')
        
        print("合併資料...")
        # 合併數據
        merged_data = pd.merge(xinpei_df, budget_df[['年', 'monthly_budget']], on='年')
        
        # 創建額外特徵
        merged_data['month'] = merged_data['date'].dt.month
        merged_data['year'] = merged_data['date'].dt.year
        merged_data['previous_month_registrations'] = merged_data['登記數'].shift(1)
        merged_data['previous_month_neutering'] = merged_data['絕育數'].shift(1)
        
        # 移除缺失值
        merged_data = merged_data.dropna()
        
        print(f"資料處理完成，共有 {len(merged_data)} 筆資料")
        return merged_data
        
    except Exception as e:
        print(f"讀取檔案時發生錯誤: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise

def train_model(data):
    # 準備特徵
    features = ['month', 'monthly_budget', '絕育數', '絕育率',
                'previous_month_registrations', 'previous_month_neutering']
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
    
    # 預測並計算指標
    predictions = model.predict(X_test_scaled)
    mape = mean_absolute_percentage_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    
    return model, scaler, predictions, y_test, mape, rmse, features

def predict_2025(model, scaler, last_data, features):
    # 準備2025年的預測數據
    future_data = pd.DataFrame()
    future_data['month'] = range(1, 13)
    future_data['monthly_budget'] = last_data['monthly_budget'].iloc[-1]  # 使用最後已知的預算
    future_data['絕育數'] = last_data['絕育數'].mean()  # 使用歷史平均值
    future_data['絕育率'] = last_data['絕育率'].mean()  # 使用歷史平均值
    future_data['previous_month_registrations'] = last_data['登記數'].mean()  # 使用歷史平均值
    future_data['previous_month_neutering'] = last_data['絕育數'].mean()  # 使用歷史平均值
    
    # 標準化特徵
    future_data_scaled = scaler.transform(future_data[features])
    
    # 預測
    predictions = model.predict(future_data_scaled)
    
    return predictions

def plot_results(actual, predicted, title):
    plt.figure(figsize=(15, 7))
    
    # 生成時間索引
    dates = pd.date_range(start='2015-1-1', periods=len(actual), freq='M')
    
    # 繪製實際值和預測值
    plt.plot(dates, actual, label='實際值', color='blue', linewidth=2)
    plt.plot(dates, predicted, label='預測值', color='orange', linewidth=2)
    
    # 設置標題和標籤
    plt.title(title, fontsize=14, pad=15)
    plt.xlabel('年月', fontsize=12)
    plt.ylabel('寵物登記數', fontsize=12)
    
    # 設置圖例
    plt.legend(prop={'size': 12}, loc='upper left')
    
    # 添加網格
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # 設置x軸刻度
    plt.gcf().autofmt_xdate()  # 自動調整日期標籤的角度
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())  # 主刻度為年
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # 主刻度格式
    plt.gca().xaxis.set_minor_locator(mdates.MonthLocator())  # 次刻度為月
    
    # 設置y軸範圍，使用千分位格式
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    # 調整邊距
    plt.tight_layout()
    
    plt.show()

def main():
    print("開始分析新北市寵物登記數據...")
    
    try:
        # 準備數據
        data = prepare_data()
        
        # 訓練模型
        print("\n開始訓練模型...")
        model, scaler, predictions, actual, mape, rmse, features = train_model(data)
        
        # 顯示模型性能
        print("\n模型性能指標：")
        print(f"MAPE (平均絕對百分比誤差): {mape:.2%}")
        print(f"RMSE (均方根誤差): {rmse:.2f}")
        print(f"平均每月預測誤差範圍: ±{rmse:.0f}個登記數")
        
        # 預測2025年數據
        print("\n進行2025年預測...")
        predictions_2025 = predict_2025(model, scaler, data, features)
        
        print("\n2025年預測結果：")
        for month, pred in enumerate(predictions_2025, 1):
            print(f"2025年{month}月預測登記數: {pred:.0f}")
        
        # 繪製結果圖表
        print("\n繪製預測結果圖表...")
        plot_results(actual, predictions, "新北市寵物登記數預測結果")
        
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