import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.preprocessing import MinMaxScaler


from sklearn.preprocessing import MinMaxScaler

def normalize_features(X):
    """
    对数据集中的特征进行归一化处理

    参数：
    X: 特征矩阵

    返回：
    X_norm: 归一化后的特征矩阵
    scaler: MinMaxScaler对象，用于反归一化
    """
    # 初始化一个MinMaxScaler对象
    scaler = MinMaxScaler()

    # 对特征进行归一化
    X_norm = scaler.fit_transform(X)

    return X_norm

# def predict_scaled_data(model, X_test, scaler):
#     """
#     Predict the target variable for the scaled test data and then
#     reverse the scaling of predicted values to get original values.
#
#     Args:
#     - model: trained regression model object
#     - X_test: numpy array or pandas DataFrame, containing test set features
#     - scaler: fitted scaler object used to normalize the data
#
#     Returns:
#     - y_pred_orig: 1D numpy array, containing predicted target variable values
#                    in their original scale
#     """
#     # Make predictions on the normalized test set
#     y_pred_norm = model.predict(X_test)
#     print(X_test.shape)
#
#     # Reverse the normalization to obtain the predictions in the original scale
#     y_pred_orig = scaler.inverse_transform(y_pred_norm.reshape(-1, 1)).flatten()
#
#     return y_pred_orig


def preprocess_data(df):
    # 对数据进行归一化处理
    scaler = MinMaxScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df.values[:,0:3]), columns=df.columns)

    # # 对数据进行标准化处理
    # df_normalized = (df_scaled - df_scaled.mean()) / df_scaled.std()

    return df_scaled, scaler
# 定义一个函数用于预测并将结果还原为原始值
def predict_and_unscale(model, X_normalized, scaler):

    # 对归一化数据进行预测
    y_normalized = model.predict(X_normalized)

    # 将预测结果还原为原始值
    y_unscaled = y_normalized * scaler.scale_[-1] + scaler.mean_[-1]

    return y_unscaled


# def preprocess_data(data_file, scale_type='standard'):
#     # 读取数据集
#     data = pd.read_csv(data_file)
#
#     # 标准化或归一化处理
#     if scale_type == 'standard':
#         scaler = StandardScaler()
#         scaled_data = scaler.fit_transform(data)
#         columns = data.columns
#     elif scale_type == 'minmax':
#         scaler = MinMaxScaler()
#         scaled_data = scaler.fit_transform(data)
#         columns = data.columns
#     else:
#         print('Invalid scale_type. Must be "standard" or "minmax".')
#         return None
#
#     # 将处理后的数据保存为DataFrame并返回
#     scaled_data = pd.DataFrame(scaled_data, columns=columns)
#     return scaled_data


def remove_outliers(df, col_num=[], threshold=3):
    """
    Remove outliers from a pandas DataFrame column using Z-score method.

    Args:
    - df: pandas DataFrame object, the input data.
    - col_name: string, the name of the column to remove outliers from.
    - threshold: float, the threshold value to determine outliers. Default is 3.

    Returns:
    - df_clean: pandas DataFrame object, the cleaned data with outliers removed.
    """

    for col_num1 in col_num:
        z_scores = np.abs((df[:,col_num1] - df[:,col_num1].mean()) / df[:,col_num1].std())
        df_clean = df[z_scores < threshold]
    return df_clean


# 读取数据集

data = pd.read_csv('./goods_traintest.csv')
datax=normalize_features(data.values[:,0:4])
datay=data.values[:,4]

data1 = np.column_stack((datax, datay))
# data1,scaler = preprocess_data(data)
print(data1)


data_clean=remove_outliers(data1,[0,1,2,3,4],3)
# data_clean=remove_outliers(data,'category',3)
# data_clean=remove_outliers(data,'original_price',3)
# data_clean=remove_outliers(data,'discount',3)


# 数据清洗和预处理
# ...

# 特征选择
features = [0, 1, 2,3]
X = data_clean[:,features]
y = data_clean[4]

# 划分训练集和测试集
train_data = []
test_data = []
for index, item in enumerate(data_clean):
    if index % 50 == 0:  # 每5条数据，第6条保留为测试集合，也就是训练集：测试集=5：1
        test_data.append(item)
    else:
        train_data.append(item)
train_data, test_data = np.array(train_data), np.array(test_data)
X_train = np.array(train_data[:, 0:4]).astype(float)
y_train = np.array(train_data[:, 4]).astype(float)
X_test = np.array(test_data[:, 0:4]).astype(float)
y_test = np.array(test_data[:, 4]).astype(float)
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# 创建线性回归模型
model = LinearRegression()

# 训练模型

model = model.fit(X_train, y_train)

# 在测试集上进行预测
y_pred = model.predict(X_test)
y_pred[y_pred < 0] = 0
for i in range(len(y_test)):
    print("true:\t{}".format(y_test[i]),end="\t")
    print("guess:\t{}".format(y_pred[i]))

# 计算均方误差和R平方值
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# 输出结果
print('均方误差：', mse)
print('R平方值：', r2)

# 绘制真实值和预测值之间的散点图
# plt.scatter(y_test, y_pred)
plt.scatter(range(len(y_test)), y_test, c='b', label='True Values')
plt.scatter(range(len(y_pred)), y_pred, c='r', label='Predicted Values')
plt.legend()
plt.xlabel('truth')
plt.ylabel('predict')
plt.title('sales_predict')
plt.show()

# 绘制ROC曲线
# ...
plt.plot(range(len(y_test)),y_test, c='black', label='y_true')
plt.plot(range(len(y_pred)),y_pred,c='red', label='y_predict')
plt.legend()
plt.show()
