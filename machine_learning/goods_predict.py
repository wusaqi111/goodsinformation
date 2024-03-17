import joblib
from machine_learning import getlist
"""
多元线性回归预测
"""
import os
from utils import dbUtil
# 加载模型

module_path = os.path.dirname(__file__)
path = module_path + '/goods.joblib'
db = dbUtil()


# 预测数据
def predict(t, p, op,le):
    subkeycat=getlist.getlist()
    category=subkeycat.index(t)+1
    preli=getlist.pred(le,category,op,p)
    model = joblib.load(path)
    pred_y = model.predict(preli)
    a=int(pred_y)
    if(a<0):
        a=0
    return "类型【" + str(t) + "】，原价【" + str(op) + "】，现价【" + str(p) + "】，预测销售量：" + '{0}'.format(a)


import matplotlib.pyplot as plt

if __name__ == '__main__':
    # Y = []
    # X = []
    # for i in range(1, 1000, 20):
    #     X.append(i)
    #     Y.append(predict("熟食", p=i, op=i))
    #
    # plt.plot(X, Y)
    # plt.ylabel('sales')
    # plt.show()
    print(predict('Apple',5199,5399,22))
