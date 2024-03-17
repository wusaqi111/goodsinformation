from utils import dbUtil
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error as MSE,r2_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import mean_squared_error, r2_score
import joblib



def getlist():
    db = dbUtil()

    cc_sql="select category from goods_subkey group by category"
    cc_res= db.query_noargs(cc_sql)
    categorycat=[]
    subkeycat=[]
    for i in cc_res:
        categorycat.append(i[0])
    for i in categorycat:
        c_sql="SELECT category,subkeycat FROM goods_subkey where category=\""+i+"\" group by subkeycat order by monthly_sales desc;"
        c_res= db.query_noargs(c_sql)
        # print(c_res)
        for ii in c_res:
            subkeycat.append(ii[1])
    db.close_commit()
    return subkeycat

def pred(le,ca,op,p):
     X_new=np.array([[float(le),float(ca),float(op),float(p)]])
     max_train=pd.read_csv('C:\\Users\\沃丝尼达耶星星\\PycharmProjects\\code\\machine_learning\\goodstrainmax.csv', dtype="float").values
     min_train=pd.read_csv('C:\\Users\\沃丝尼达耶星星\\PycharmProjects\\code\\machine_learning\\goodstrainmin.csv', dtype="float").values

     # temp1=np.array(temp).astype(float)
     # feature=normalize_features(temp1)
     X_new_norm = (X_new - min_train) / (max_train - min_train)
     pp = PolynomialFeatures(degree=3)
     d_2_feature = pp.fit_transform(X_new_norm)
     return d_2_feature