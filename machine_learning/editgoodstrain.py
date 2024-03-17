from utils import dbUtil
import datetime
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
        sqll1="select count(id) from category_new where category=\""+ ii[0] +"\" and subkey=\""+ii[1]+"\""
        sssdep=db.query_noargs(sqll1)
        subkeycat.append(ii[1])
        if(sssdep[0][0]==0):
            sqlins="insert into category_new VALUES (NULL, \""+ii[0]+"\",\""+ii[1]+"\")"
            db.query_noargs(sqlins)
s_sql="select * from goods_subkey"
s_res= db.query_noargs(s_sql)
# sqll1="select subkey from category_new where=\""
# # category插入
# for i in categorycat:
#     for ii in subkeycat:
#         sqll1="select count(id) from category_new where subkey=\""+ii+"\""
#         sssdep=db.query_noargs(sqlins)
#         if(sssdep[0][0]==0):
#             sqlins="insert into category_new VALUES (NULL, \""+i+"\",\""+ii+"\")"
#             db.query_noargs(sqlins)
#
# print(s_res)
m = datetime.datetime.now().strftime("%Y-%m")
level=0
print(s_res[0])
for ii in s_res:
    if(int(ii[8])>=0 and int(ii[8])<10):
        level=1
    if(int(ii[8])>=10 and int(ii[8])<20):
        level=2
    if(int(ii[8])>=20 and int(ii[8])<30):
        level=3
    if(int(ii[8])>=30 and int(ii[8])<40):
        level=4
    if(int(ii[8])>=40 and int(ii[8])<50):
        level=5
    if(int(ii[8])>=50 and int(ii[8])<60):
        level=6
    if(int(ii[8])>=60 and int(ii[8])<70):
        level=7
    if(int(ii[8])>=70 and int(ii[8])<80):
        level=8
    if(int(ii[8])>=80 and int(ii[8])<90):
        level=9
    if(int(ii[8])>=90 and int(ii[8])<100):
        level=10
    if(int(ii[8])>=100 and int(ii[8])<200):
        level=11
    if(int(ii[8])>=200 and int(ii[8])<300):
        level=12
    if(int(ii[8])>=300 and int(ii[8])<400):
        level=13
    if(int(ii[8])>=400 and int(ii[8])<500):
        level=14
    if(int(ii[8])>=500 and int(ii[8])<600):
        level=15
    if(int(ii[8])>=600 and int(ii[8])<700):
        level=16
    if(int(ii[8])>=700 and int(ii[8])<800):
        level=17
    if(int(ii[8])>=800 and int(ii[8])<900):
        level=18
    if(int(ii[8])>=900 and int(ii[8])<1000):
        level=19
    if(int(ii[8])>=1000 and int(ii[8])<2000):
        level=20
    if(int(ii[8])>=2000 and int(ii[8])<3000):
        level=21
    if(int(ii[8])>=3000 and int(ii[8])<4000):
        level=22
    if(int(ii[8])>=4000 and int(ii[8])<5000):
        level=23
    if(int(ii[8])>=5000 and int(ii[8])<6000):
        level=24
    if(int(ii[8])>=6000 and int(ii[8])<7000):
        level=25
    if(int(ii[8])>=7000 and int(ii[8])<8000):
        level=26
    if(int(ii[8])>=8000 and int(ii[8])<9000):
        level=27
    if(int(ii[8])>=9000 and int(ii[8])<10000):
        level=28
    if(int(ii[8])>=10000 and int(ii[8])<20000):
        level=29
    if(int(ii[8])>=20000 and int(ii[8])<30000):
        level=30
    if(int(ii[8])>=30000 and int(ii[8])<40000):
        level=31
    if(int(ii[8])>=40000 and int(ii[8])<50000):
        level=32
    if(int(ii[8])>=50000):
        level=33
    category=subkeycat.index(ii[4])+1
    ii=list(ii)
    # for id,pid, title,categoryy,subkeycat, discount, original_price, shop, monthly_sales,m in ii:
    # ss_sql = "select count(id) from goods_train where  pid=\"" + ii[1] +"\""
    ss_sql = "select count(id) from goods_train where pid=\"" + ii[1] + "\" and monthly=\"" + m + "\" and monthly_sales=\"" + str(ii[8] )+"\""
    ss_res = db.query_noargs(ss_sql)
    if ss_res[0][0] == 0:
        goods_sql = "insert into goods_train VALUES (NULL, \"" + ii[1] + "\", \"" + ii[2] + "\",\"" + str(category) + "\"," + str(
            ii[5]) + "," + str(ii[6]) + ",\"" + str(level) + "\"," + str(ii[8]) + ",\"" + ii[9] +"\", \""+ ii[3] +"\")"
        db.query_noargs(goods_sql)
        # (1, '4179235765', 'Apple/苹果 iPhone 14 Pro', '手机', 'Apple', Decimal('7999.00'), Decimal('7999.00'), 'Apple Store 官方旗舰店', 20000, '2023-04')

db.close_commit()