from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import urllib.parse
from selenium.common.exceptions import WebDriverException
from pyquery import PyQuery as pq
from utils import dbUtil
import datetime
import json
import time
import random
from browsermobproxy import Server
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import re
import numpy as np
db = dbUtil()
cc_sql="select category from goods_subkey group by category"

# c_sql="select count(id) from category where content=\"" + subkeycat + "\""
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
        sqlins="insert into category_new VALUES (NULL, \""+ii[0]+"\",\""+ii[1]+"\")"
        db.query_noargs(sqlins)
s_sql="select * from goods_subkey"
s_res= db.query_noargs(s_sql)
# category插入
# for i in categorycat:
#     for ii in subkeycat:
#         sqlins="insert into category_new VALUES (NULL, \""+i+"\",\""+ii+"\")"
#         db.query_noargs(sqlins)

# print(s_res)
m = datetime.datetime.now().strftime("%Y-%m")
for ii in s_res:
    category=subkeycat.index(ii[4])+1
    ii=list(ii)
    # for id,pid, title,categoryy,subkeycat, discount, original_price, shop, monthly_sales,m in ii:
    # ss_sql = "select count(id) from goods_train where  pid=\"" + ii[1] +"\""
    ss_sql = "select count(id) from goods_train where pid=\"" + ii[1] + "\" and monthly=\"" + m + "\" and shop=\"" + ii[7] + "\" and monthly_sales=\"" + str(ii[8] )+"\""
    ss_res = db.query_noargs(ss_sql)
    print(ss_res[0][0])
    if ss_res[0][0] == 0:
        goods_sql = "insert into goods_train VALUES (NULL, \"" + ii[1] + "\", \"" + ii[2] + "\",\"" + str(category) + "\"," + str(
            ii[5]) + "," + str(ii[6]) + ",\"" + ii[7] + "\"," + str(ii[8]) + ",\"" + ii[9] +"\", \""+ ii[3] +"\")"
        db.query_noargs(goods_sql)
# print(subkeycat)
db.close_commit()