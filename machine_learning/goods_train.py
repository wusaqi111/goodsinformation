from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import joblib

data = pd.read_csv("./goods_trainultt.csv", dtype="str").values
# 分割数据集合
listnum=[]
train_data = []
test_data = []
a=0
for index, item in enumerate(data):
    # print("index:",index,"item:",item)
    if index % 5 == 0:  # 每5条数据，第6条保留为测试集合，也就是训练集：测试集=5：1
        if(item[0] not in listnum):
            listnum.append(item[0])
            a=item[0]
            if(train_data):
                train_data, test_data = np.array(train_data), np.array(test_data)
                X = np.array(train_data[:, 0:4]).astype(float)
                Y = np.array(train_data[:, 4]).astype(float)
                test_X = np.array(test_data[:, 0:4]).astype(float)
                text_Y = np.array(test_data[:, 4]).astype(float)
                # 定义算法模型
                model = LinearRegression()
                # 喂入模型数据
                model.fit(X, Y)
                if(a==listnum[- 2]):
                    joblib.dump(model, "./goods{0}.joblib".format(listnum[-2]))
                else:
                    joblib.dump(model, "./goods{0}.joblib".format(listnum[-1]))
                # 测试集上模型评分
                print("[INFO] 模型EMS损失值（模型评分越低越好）：", abs(model.score(test_X, text_Y)))
                print("[INFO] 多元线性回归预测销量-训练完成")
                train_data = []
                test_data = []
        test_data.append(item)
    else:
        if(item[0] not in listnum):
            listnum.append(item[0])
            a=item[0]
            if(test_data):
                train_data, test_data = np.array(train_data), np.array(test_data)
                X = np.array(train_data[:, 0:4]).astype(float)
                Y = np.array(train_data[:, 4]).astype(float)
                test_X = np.array(test_data[:, 0:4]).astype(float)
                text_Y = np.array(test_data[:, 4]).astype(float)
                # 定义算法模型
                model = LinearRegression()
                # 喂入模型数据
                model.fit(X, Y)
                if(a==listnum[-2]):
                    joblib.dump(model, "./goods{0}.joblib".format(listnum[-2]))
                else:
                    joblib.dump(model, "./goods{0}.joblib".format(listnum[-1]))
                print("[INFO] 模型EMS损失值（模型评分越低越好）：", abs(model.score(test_X, text_Y)))
                print("[INFO] 多元线性回归预测销量-训练完成")
                train_data = []
                test_data = []
        train_data.append(item)
# for index, item in enumerate(data):
#     print(index)







