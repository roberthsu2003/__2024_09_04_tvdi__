import joblib
import numpy as np

# 定義新的輸入數據（確保格式與訓練數據一致）
new_data = [[0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]]

# 載入三種不同的模型
models = {
    '推薦': joblib.load('trained_model.pkl'),
}

# 重複多次預測，查看結果的一致性
for method, model in models.items():
    print(f"\n{method}連續預測：")
    for _ in range(5):
        predicted = model.predict(new_data)
        print(f"預測值: {predicted[0]:.3f}")
