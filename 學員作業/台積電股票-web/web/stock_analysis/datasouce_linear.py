import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import datetime as dt
import pandas_datareader as web
import requests
import yfinance as yf
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import SGDRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score


# 讀取歷史數據
start = dt.datetime(2022, 1, 1)
end = dt.datetime(2024, 11, 1)
data = yf.download('2330.TW', start=start, end=end)

# 將索引轉換為日期格式
data['Date'] = pd.to_datetime(data.index)
# 將日期轉換為從最早日期起的天數
data['Days'] = (data['Date'] - data['Date'].min()).dt.days

X = data[['Days']]  # 自變量
y = data['Close']  # 目標變量

# 線性回歸模型

'''
LinearRegression

SGDRegressor
model = SGDRegressor()
model.fit(X, y.values.ravel())



fit_intercept: 預設為True，表示有將y軸的截距加入 ，並自動計算出最佳的截距值 ，如果為False，迴歸模型線會直接通過原點
normalize : 是否將數據做歸一化（Normalize），預設為False
copy_X : 預設為True，表示X會被Copied，如果為False，X會被覆蓋掉
n_jobs : 計算模型所使使用的CPU數量，預設為1，如果傳入-1，就會使用全部的CPU


'''
# scaler = StandardScaler()
# X_scarled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.4, random_state = 0)
model = LinearRegression(fit_intercept=True,copy_X=True,n_jobs=1)
model.fit(X_train, y_train)
model_score = model.score(X_train, y_train)
b = model.intercept_
a = model.coef_
   
    
print(f'Model Score (R²): {model_score:.4f}\nCoeficient: {a} \nIntercept: {b}')
print("=========================================")
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test,y_pred)
r2 = r2_score(y_test,y_pred)
print(f'Model Score (R²): {r2:.4f}\nMean Squared Error: {mse}')




# 繪圖
plt.figure(figsize=(12, 6))
plt.plot(data['Date'], data['Close'], label='Historical Close Price', color='Blue')

# 使用 model 預測的值
plt.plot(data['Date'], model.predict(X), label='Linear Regression', color='orange')

# 進行預測
# 未來30天
future_days = 30

# 獲取最後一個日期的天數
last_day = data['Date'].max()
# 使用模型進行預測
future_x = np.arange(data['Days'].max() + 1, data['Days'].max() + future_days + 1).reshape(-1, 1)
predicted_price = model.predict(future_x)

# 將預測結果轉換為日期格式，從最後一天開始
future_dates = [last_day + pd.Timedelta(days=i) for i in range(1, future_days + 1)]

# 顯示預測價格
plt.plot(future_dates, predicted_price, label='Future Prediction', color='red', linestyle='--')

# 設定
plt.xlim(pd.Timestamp('2020-01-01'), future_dates[-1])
plt.xlabel('Date')
plt.ylabel('Close Price')

#plt.ylim(min(data['Close'].iloc[0].min(),predicted_price.min())-10,max(data['Close'].iloc[0].max(),predicted_price.max())+10)
plt.ylim(0,1500)
plt.title('Close Price and Linear Regression Line with Prediction')

plt.legend()
plt.show()
