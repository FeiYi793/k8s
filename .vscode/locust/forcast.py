import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

# 创建一个简单的时间序列数据集
np.random.seed(42)
date_rng = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
data = np.random.randint(0, 100, size=(len(date_rng)))
time_series = pd.Series(data, index=date_rng)

# 数据预处理
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(np.array(time_series).reshape(-1, 1))

# 将时间序列数据转换为监督学习问题
def create_dataset(dataset, time_steps=1):
    X, y = [], []
    for i in range(len(dataset) - time_steps):
        a = dataset[i:(i + time_steps), 0]
        X.append(a)
        y.append(dataset[i + time_steps, 0])
    return np.array(X), np.array(y)

time_steps = 10  # 可调整的时间步数
X, y = create_dataset(scaled_data, time_steps)

# 划分数据集为训练集和测试集
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# 构建RNN模型
model = Sequential()
model.add(SimpleRNN(50, input_shape=(time_steps, 1)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

# 训练模型
model.fit(X_train.reshape((X_train.shape[0], X_train.shape[1], 1)), y_train, epochs=50, batch_size=32, verbose=2)

# 在测试集上进行预测
predictions = model.predict(X_test.reshape((X_test.shape[0], X_test.shape[1], 1)))
predictions = scaler.inverse_transform(predictions)

# 计算均方根误差（RMSE）
rmse = np.sqrt(mean_squared_error(time_series.iloc[train_size + time_steps:], predictions))
print(f'Root Mean Squared Error (RMSE): {rmse}')

# 可视化预测结果
plt.plot(time_series.index[train_size + time_steps:], time_series.iloc[train_size + time_steps:], label='Observed')
plt.plot(time_series.index[train_size + time_steps:], predictions, label='Predicted', linestyle='dashed')
plt.title('RNN Time Series Forecasting')
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()
plt.show()
