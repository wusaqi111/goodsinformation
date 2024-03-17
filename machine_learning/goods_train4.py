import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
import pandas as pd
from sklearn import datasets
import seaborn as sns
import csv
from matplotlib.pylab import mpl
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split #这里是引用了交叉验证
from sklearn.linear_model import LinearRegression  #线性回归

def display_lr():
    pd_data=pd.read_csv('./goods_traintest.csv', dtype="float")#原始数表
    #画出单因素拟合情况
    print('pd_data.head(10)=\n{}'.format(pd_data.head(10000)))
    # mpl.rcParams['font.sans-serif'] = ['SimHei']  #配置显示中文，否则乱码
    mpl.rcParams['axes.unicode_minus']=False #用来正常显示负号，如果是plt画图，则将mlp换成plt
    sns.pairplot(pd_data, x_vars=['category','discount','original_price'], y_vars='monthly_sales',kind="reg", size=5, aspect=0.7)
    plt.show()

def Normalization():
    #对数据进行归一化处理 并存储到eth2.csv

    pd_data=pd.read_csv('./goods_trainphone.csv', dtype="float")
    # scaler = MinMaxScaler()
    # result_ = scaler.fit_transform(pd_data)
    # print(result_)
    sam=[]
    a=['category','discount','original_price']
    for i in a:
        y = pd_data.loc[:, i]
        ys = list(preprocessing.scale(y))  # 归一化
        sam.append(ys)


    # print(sam[3])
    with open('./goods_train1.csv', 'w',newline='') as file:
        writer = csv.writer(file)
        writer.writerow(a)
        for i in range(len(sam[3])):
            writer.writerow([sam[0][i],sam[1][i],sam[2][i],sam[3][i]])
    print('完毕')

def build_lr():
    train_data = []
    test_data = []
    pd_data=pd.read_csv('./goods_traintest.csv', dtype="float").values
    # X = pd_data.loc[:, ('category','discount','original_price')]
    # y = pd_data.loc[:, 'monthly_sales']
    for index, item in enumerate(pd_data):
        if index % 10 == 0:  # 每5条数据，第6条保留为测试集合，也就是训练集：测试集=5：1
            test_data.append(item)
        else:
            train_data.append(item)
    train_data, test_data = np.array(train_data), np.array(test_data)
    print(pd_data)
    X_train = np.array(train_data[:, 0:4]).astype(float)
    y_train = np.array(train_data[:, 4]).astype(float)
    X_test = np.array(test_data[:, 0:4]).astype(float)
    y_test = np.array(test_data[:, 4]).astype(float)
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=532)#选择20%为测试集
    # for i in range(len(X)):
    #     if(i % 5==0):
    #         test_x.append(x_data[ii])
    print('训练集测试及参数:')
    print('X_train.shape={}\n y_train.shape ={}\n X_test.shape={}\n,  y_test.shape={}'.format(X_train.shape,
                                                                                              y_train.shape,
                                                                                              X_test.shape,
                                                                                              y_test.shape))
    linreg = LinearRegression()
    #训练
    model = linreg.fit(X_train, y_train)
    print('模型参数:')
    print(model)
    # 训练后模型截距
    print('模型截距:')
    print (linreg.intercept_)
    # 训练后模型权重（特征个数无变化）
    print('参数权重:')
    print (linreg.coef_)

    y_pred = linreg.predict(X_test)
    sum_mean = 0
    for i in range(len(y_pred)):
        sum_mean += (y_pred[i] - y_test[i]) ** 2
    sum_erro = np.sqrt(sum_mean /len(y_pred))  # 测试级的数量
    # calculate RMSE
    print ("RMSE by hand:", sum_erro)
    # 做ROC曲线
    plt.figure()
    plt.plot(range(len(y_pred)), y_pred, 'b', label="predict")
    plt.plot(range(len(y_pred)), y_test, 'r', label="test")
    plt.legend(loc="upper right")  # 显示图中的标签
    plt.xlabel("the number of sales")
    plt.ylabel('value of sales')
    plt.show()

if __name__ == '__main__':
    display_lr()