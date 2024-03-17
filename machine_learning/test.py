import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error as MSE,r2_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import csv
import matplotlib.pyplot as plt
import seaborn as sns

def heatmap(df):
    # 取出特征值和目标值
    X = df[:, :4]
    y = df[:, 4]

    # 计算相关系数矩阵
    corr_matrix = np.corrcoef(np.column_stack((X, y)).T)

    # 绘制热力图
    fig, ax = plt.subplots()
    im = ax.imshow(corr_matrix, cmap='coolwarm')

    # 设置刻度
    ax.set_xticks(np.arange(X.shape[1] + 1))
    ax.set_yticks(np.arange(X.shape[1] + 1))
    ax.set_xticklabels(['feature_1', 'feature_2', 'feature_3', 'feature_4', 'target'])
    ax.set_yticklabels(['feature_1', 'feature_2', 'feature_3', 'feature_4', 'target'])
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    # 显示每一块的相关系数
    for i in range(X.shape[1]):
        for j in range(X.shape[1] + 1):
            text = ax.text(j, i, round(corr_matrix[i, j], 2),
                           ha="center", va="center", color="w")

    # 显示颜色条
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel('correlation', rotation=-90, va="bottom")

    # 显示热力图
    plt.show()


def normalize_features1(X):
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
    min_train = scaler.data_min_
    max_train = scaler.data_max_
    a=['1','2','3','4']
    with open('./goodstrainmax.csv', 'w',newline='') as file:
        writer = csv.writer(file)
        writer.writerow(a)
        writer.writerow([max_train[0],max_train[1],max_train[2],max_train[3]])
    with open('./goodstrainmin.csv', 'w',newline='') as file:
        writer = csv.writer(file)
        writer.writerow(a)
        writer.writerow([min_train[0],min_train[1],min_train[2],min_train[3]])
    # print('完毕')

    return X_norm


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

# 1.导入数据
df = pd.read_csv('./goods_traintest.csv').values
# df.head(0)

df1=remove_outliers(df, [0,1,2,3,4], threshold=3)
# 2.提取样本数据
feature1 = df1[:,0:4]
feature=normalize_features(feature1)
print("归一化前：",feature1)
print("归一化后：",feature)
target = df1[:,4]

degrees = [1, 2, 3, 4] # 多项式阶数范围
kf = KFold(n_splits=5, shuffle=True, random_state=2021) # 交叉验证分割器
mse_mean = []
mse_std = []

for degree in degrees:
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    X_poly = poly.fit_transform(feature)
    X_poly = normalize_features1(X_poly)
    mse = []

    for train_index, test_index in kf.split(X_poly):
        X_train, X_test = X_poly[train_index], X_poly[test_index]
        y_train, y_test = target[train_index], target[test_index]
        lr = LinearRegression()
        lr.fit(X_train, y_train)
        y_pred = lr.predict(X_test)
        mse.append(mean_squared_error(y_test, y_pred))

    mse_mean.append(np.mean(mse))
    mse_std.append(np.std(mse))
# 绘制交叉验证的mse均值和标准差随多项式阶数的变化曲线
plt.errorbar(degrees, mse_mean, fmt='-o')
plt.title('Cross Validation')
plt.xlabel('Degree of Polynomial')
plt.ylabel('MSE')
plt.show()


# 输出最优degree
opt_degree = degrees[np.argmin(mse_mean)]
print('Optimal degree of polynomial regression:', opt_degree)

# 3.给原始特征增加高次特征
p = PolynomialFeatures(degree=3)
d_2_feature = p.fit_transform(feature)
print("原始特征",feature)
print("拓展后特征",d_2_feature)
d_2_feature=d_2_feature.tolist()
# print(d_2_feature)
# print(d_2_feature.shape)  # (414, 28)
# target.shape  # (414,)

# 4.切分样本数据
# x_train,x_test,y_train,y_test = train_test_split(d_2_feature,target,test_size=0.2, random_state=2020)
train_data = []
train_datay=[]
test_data = []
test_datay = []
for i in range(len(d_2_feature)):
    if i % 50 == 0:  # 每20条数据，第21条保留为测试集合，也就是训练集：测试集=5：1
        test_data.append(d_2_feature[i])
        test_datay.append(target[i])
    else:
        train_data.append(d_2_feature[i])
        train_datay.append(target[i])
train_data, test_data = np.array(train_data), np.array(test_data)
x_train = np.array(train_data).astype(float)
y_train = np.array(train_datay).astype(float)

x_test = np.array(test_data).astype(float)
y_test = np.array(test_datay).astype(float)
