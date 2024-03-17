from flask import jsonify
from utils import dbUtil


# 获取页面总计数据
def total_data(c,s): #c大类 s小类品牌
    db = dbUtil()
    # if(c=='' and s==''):
    if(c==''):
        goods_count_sql = "SELECT count(1) FROM goods_subkey"
        shop_count_sql = "SELECT count(1) FROM (select shop from goods_subkey group by shop) as t"
        category_count_sql = "SELECT count(1) FROM (select category from goods_subkey group by category) as t "
        goods_count = db.query_noargs(goods_count_sql)[0][0]
        shop_count = db.query_noargs(shop_count_sql)[0][0]
        category_count = db.query_noargs(category_count_sql)[0][0]
    # else:
    #     if(c==''):
    #         goods_count_sql = "SELECT count(1) FROM goods_subkey where subkeycat='"+s+"';"
    #         # sql1="where category="+ +""
    #         shop_count_sql = "SELECT count(1) FROM (select shop from goods_subkey where subkeycat='"+s+"' group by shop) as t"
    #         category_count_sql = "SELECT count(1) FROM (select category from goods_subkey where subkeycat='"+s+"' group by category) as t "
    #         # goods_count = db.query_noargs(goods_count_sql)[0][0]
    #         # shop_count = db.query_noargs(shop_count_sql)[0][0]
    #         # category_count = db.query_noargs(category_count_sql)[0][0]
    elif(s==''):
        goods_count_sql = "SELECT count(1) FROM goods_subkey where category='"+c+"';"
        # sql1="where category="+ +""
        shop_count_sql = "SELECT count(1) FROM (select shop from goods_subkey where category='"+c+"' group by shop) as t"
        category_count_sql = "SELECT count(1) FROM (select category from goods_subkey where category='"+c+"' group by category) as t "
        goods_count = db.query_noargs(goods_count_sql)[0][0]
        shop_count = db.query_noargs(shop_count_sql)[0][0]
        category_count = db.query_noargs(category_count_sql)[0][0]
    else:
        goods_count_sql = "SELECT count(1) FROM goods_subkey where category='"+c+"'and subkeycat='"+s+"';"
        shop_count_sql = "SELECT count(1) FROM (select shop from goods_subkey where category='"+c+"' and  subkeycat='"+s+"'group by shop) as t"
        category_count_sql = "SELECT count(1) FROM (select category from goods_subkey where category='"+c+"' and subkeycat='"+s+"' group by category) as t "
        goods_count = db.query_noargs(goods_count_sql)[0][0]
        shop_count = db.query_noargs(shop_count_sql)[0][0]
        category_count = db.query_noargs(category_count_sql)[0][0]
    db.close()
    # print('inf',goods_count,shop_count,category_count)
    return jsonify({"goods": goods_count, "shop": shop_count, "category": category_count})


# 商品销量top10
def goods_sales_top(c,s):
    if(c==''):
        goods_top_sql = "select left(title,6),monthly_sales FROM goods_subkey ORDER BY monthly_sales desc limit 10;"
    # else:
    #     if(c==''):
    #         goods_top_sql = "select left(title,6),monthly_sales FROM goods_subkey where subkeycat='"+s+"' ORDER BY monthly_sales desc limit 10;"
    elif(s==''):
        goods_top_sql = "select left(title,6),monthly_sales FROM goods_subkey where category='"+c+"' ORDER BY monthly_sales desc limit 10;"
    else:
        goods_top_sql = "select left(title,6),monthly_sales FROM goods_subkey where subkeycat='"+s+"' and category='"+c+"' ORDER BY monthly_sales desc limit 10;"
    data = []
    db = dbUtil()
    goods_top_res = db.query_noargs(goods_top_sql)
    for a, b in goods_top_res:
        item = {"time": a, "value": b, "name": "商品销量TOP10"}
        data.append(item)
    db.close()
    return jsonify({"data": data})


# 商铺销量top10
def shop_sales_top(c,s):
    if(c==''):
        shop_top_sql = "select left(shop,6),SUM(monthly_sales)  FROM goods_subkey GROUP BY shop ORDER BY SUM(monthly_sales) desc limit 10"
    # else:
    #     if(c==''):
    #         shop_top_sql = "select left(shop,6),SUM(monthly_sales)  FROM goods_subkey where subkeycat='"+s+"' GROUP BY shop ORDER BY SUM(monthly_sales) desc limit 10"
    elif(s==''):
        shop_top_sql = "select left(shop,6),SUM(monthly_sales)  FROM goods_subkey where category='"+c+"' GROUP BY shop ORDER BY SUM(monthly_sales) desc limit 10"
    else:
        shop_top_sql = "select left(shop,6),SUM(monthly_sales)  FROM goods_subkey where category='"+c+"' and subkeycat='"+s+"' GROUP BY shop ORDER BY SUM(monthly_sales) desc limit 10"
    data = []
    db = dbUtil()
    shop_top_res = db.query_noargs(shop_top_sql)
    for a, b in shop_top_res:
        item = {"time": a, "value": b, "name": "店铺销量TOP10"}
        data.append(item)
    db.close()
    return jsonify({"data": data})


# 销量分布
def sales_distribution_data(c,s):
    # sql_1 = "SELECT count(1) FROM goods WHERE monthly_sales >=0 AND monthly_sales<50;"
    # sql_2 = "SELECT count(1) FROM goods WHERE monthly_sales >=50 AND monthly_sales<100;"
    # sql_3 = "SELECT count(1) FROM goods WHERE monthly_sales >=100 AND monthly_sales<500;"
    # sql_4 = "SELECT count(1) FROM goods WHERE monthly_sales >=500 AND monthly_sales<1000;"
    # sql_5 = "SELECT count(1) FROM goods WHERE monthly_sales >=1000 AND monthly_sales<10000;"
    # sql_6 = "SELECT count(1) FROM goods WHERE monthly_sales >=10000;"
    if(c==''):
        sql_1 = "SELECT count(1) FROM goods_subkey WHERE monthly_sales >=0 AND monthly_sales<50;"
        sql_2 = "SELECT count(1) FROM goods_subkey WHERE monthly_sales >=50 AND monthly_sales<100;"
        sql_3 = "SELECT count(1) FROM goods_subkey WHERE monthly_sales >=100 AND monthly_sales<500;"
        sql_4 = "SELECT count(1) FROM goods_subkey WHERE monthly_sales >=500 AND monthly_sales<1000;"
        sql_5 = "SELECT count(1) FROM goods_subkey WHERE monthly_sales >=1000 AND monthly_sales<10000;"
        sql_6 = "SELECT count(1) FROM goods_subkey WHERE monthly_sales >=10000;"
    # else:
    #     if(c==''):
    #         sql_1 = "SELECT count(1) FROM goods_subkey WHERE subkeycat='"+s+"' AND monthly_sales >=0 AND monthly_sales<50;"
    #         sql_2 = "SELECT count(1) FROM goods_subkey WHERE subkeycat='"+s+"' AND monthly_sales >=50 AND monthly_sales<100;"
    #         sql_3 = "SELECT count(1) FROM goods_subkey WHERE subkeycat='"+s+"' AND monthly_sales >=100 AND monthly_sales<500;"
    #         sql_4 = "SELECT count(1) FROM goods_subkey WHERE subkeycat='"+s+"' AND monthly_sales >=500 AND monthly_sales<1000;"
    #         sql_5 = "SELECT count(1) FROM goods_subkey WHERE subkeycat='"+s+"' AND monthly_sales >=1000 AND monthly_sales<10000;"
    #         sql_6 = "SELECT count(1) FROM goods_subkey WHERE subkeycat='"+s+"' AND monthly_sales >=10000;"
    elif(s==''):
        sql_1 = "SELECT count(1) FROM goods_subkey WHERE category='"+c+"' AND monthly_sales >=0 AND monthly_sales<50;"
        sql_2 = "SELECT count(1) FROM goods_subkey WHERE category='"+c+"' AND monthly_sales >=50 AND monthly_sales<100;"
        sql_3 = "SELECT count(1) FROM goods_subkey WHERE category='"+c+"' AND monthly_sales >=100 AND monthly_sales<500;"
        sql_4 = "SELECT count(1) FROM goods_subkey WHERE category='"+c+"' AND monthly_sales >=500 AND monthly_sales<1000;"
        sql_5 = "SELECT count(1) FROM goods_subkey WHERE category='"+c+"' AND monthly_sales >=1000 AND monthly_sales<10000;"
        sql_6 = "SELECT count(1) FROM goods_subkey WHERE category='"+c+"' AND monthly_sales >=10000;"
    else:
        sql_1 = "SELECT count(1) FROM goods_subkey WHERE category='"+c+"' AND subkeycat='"+s+"' AND monthly_sales >=0 AND monthly_sales<50;"
        sql_2 = "SELECT count(1) FROM goods_subkey WHERE category='"+c+"' AND subkeycat='"+s+"' AND monthly_sales >=50 AND monthly_sales<100;"
        sql_3 = "SELECT count(1) FROM goods_subkey WHERE category='"+c+"' AND subkeycat='"+s+"'AND monthly_sales >=100 AND monthly_sales<500;"
        sql_4 = "SELECT count(1) FROM goods_subkey WHERE category='"+c+"' AND subkeycat='"+s+"'AND monthly_sales >=500 AND monthly_sales<1000;"
        sql_5 = "SELECT count(1) FROM goods_subkey WHERE category='"+c+"' AND subkeycat='"+s+"'AND monthly_sales >=1000 AND monthly_sales<10000;"
        sql_6 = "SELECT count(1) FROM goods_subkey WHERE category='"+c+"' AND subkeycat='"+s+"'AND monthly_sales >=10000;"
    db = dbUtil()
    c_1 = db.query_noargs(sql_1)[0][0]
    c_2 = db.query_noargs(sql_2)[0][0]
    c_3 = db.query_noargs(sql_3)[0][0]
    c_4 = db.query_noargs(sql_4)[0][0]
    c_5 = db.query_noargs(sql_5)[0][0]
    c_6 = db.query_noargs(sql_6)[0][0]
    return jsonify(
        {"data": [{"name": "0-50", "value": c_1}, {"name": "50-100", "value": c_2}, {"name": "100-500", "value": c_3},
                  {"name": "500-1000", "value": c_4}, {"name": "1000-10000", "value": c_5},
                  {"name": "10000+", "value": c_6}]})


# 销售价格分布
def price_distribution_data(c,s):
    # sql_1 = "SELECT count(1) FROM goods WHERE monthly_sales >=0 AND monthly_sales<50;"
    # sql_2 = "SELECT count(1) FROM goods WHERE discount >=100 AND discount<500;"
    # sql_3 = "SELECT count(1) FROM goods WHERE discount >=500 AND discount<1000;"
    # sql_4 = "SELECT count(1) FROM goods WHERE discount >=1000 AND discount<5000;"
    # sql_5 = "SELECT count(1) FROM goods WHERE discount >=5000 AND discount<10000;"
    # sql_6 = "SELECT count(1) FROM goods WHERE discount >=10000;"
    if(c==''):
        sql_1 = "SELECT count(1) FROM goods_subkey WHERE monthly_sales >=0 AND monthly_sales<50;"
        sql_2 = "SELECT count(1) FROM goods_subkey WHERE discount >=100 AND discount<500;"
        sql_3 = "SELECT count(1) FROM goods_subkey WHERE discount >=500 AND discount<1000;"
        sql_4 = "SELECT count(1) FROM goods_subkey WHERE discount >=1000 AND discount<5000;"
        sql_5 = "SELECT count(1) FROM goods_subkey WHERE discount >=5000 AND discount<10000;"
        sql_6 = "SELECT count(1) FROM goods_subkey WHERE discount >=10000;"
    # else:
    #     if(c==''):
    #         sql_1 = "SELECT count(1) FROM goods_subkey WHERE subkeycat='"+s+"' AND monthly_sales >=0 AND monthly_sales<50;"
    #         sql_2 = "SELECT count(1) FROM goods_subkey WHERE subkeycat='"+s+"' AND discount >=100 AND discount<500;"
    #         sql_3 = "SELECT count(1) FROM goods_subkey WHERE subkeycat='"+s+"' AND discount >=500 AND discount<1000;"
    #         sql_4 = "SELECT count(1) FROM goods_subkey WHERE subkeycat='"+s+"' AND discount >=1000 AND discount<5000;"
    #         sql_5 = "SELECT count(1) FROM goods_subkey WHERE subkeycat='"+s+"' AND discount >=5000 AND discount<10000;"
    #         sql_6 = "SELECT count(1) FROM goods_subkey WHERE subkeycat='"+s+"' AND discount >=10000;"
    elif(s==''):
        sql_1 = "SELECT count(1) FROM goods_subkey WHERE category='"+c+"' AND monthly_sales >=0 AND monthly_sales<50;"
        sql_2 = "SELECT count(1) FROM goods_subkey WHERE category='"+c+"' AND discount >=100 AND discount<500;"
        sql_3 = "SELECT count(1) FROM goods_subkey WHERE category='"+c+"' AND discount >=500 AND discount<1000;"
        sql_4 = "SELECT count(1) FROM goods_subkey WHERE category='"+c+"' AND discount >=1000 AND discount<5000;"
        sql_5 = "SELECT count(1) FROM goods_subkey WHERE category='"+c+"' AND discount >=5000 AND discount<10000;"
        sql_6 = "SELECT count(1) FROM goods_subkey WHERE category='"+c+"' AND discount >=10000;"
    else:
        sql_1 = "SELECT count(1) FROM goods_subkey WHERE category='"+c+"' AND subkeycat='"+s+"' AND monthly_sales >=0 AND monthly_sales<50;"
        sql_2 = "SELECT count(1) FROM goods_subkey WHERE category='"+c+"' AND subkeycat='"+s+"' AND discount >=100 AND discount<500;"
        sql_3 = "SELECT count(1) FROM goods_subkey WHERE category='"+c+"' AND subkeycat='"+s+"' AND discount >=500 AND discount<1000;"
        sql_4 = "SELECT count(1) FROM goods_subkey WHERE category='"+c+"' AND subkeycat='"+s+"' AND discount >=1000 AND discount<5000;"
        sql_5 = "SELECT count(1) FROM goods_subkey WHERE category='"+c+"' AND subkeycat='"+s+"' AND discount >=5000 AND discount<10000;"
        sql_6 = "SELECT count(1) FROM goods_subkey WHERE category='"+c+"' AND subkeycat='"+s+"' AND discount >=10000;"
    db = dbUtil()
    c_1 = db.query_noargs(sql_1)[0][0]
    c_2 = db.query_noargs(sql_2)[0][0]
    c_3 = db.query_noargs(sql_3)[0][0]
    c_4 = db.query_noargs(sql_4)[0][0]
    c_5 = db.query_noargs(sql_5)[0][0]
    c_6 = db.query_noargs(sql_6)[0][0]
    return jsonify({"data": [{"name": "0-100", "value": c_1}, {"name": "100-500", "value": c_2},
                             {"name": "500-1000", "value": c_3},
                             {"name": "1000-5000", "value": c_4}, {"name": "5000-10000", "value": c_5},
                             {"name": "10000+", "value": c_6}]})


# 类别统计
def category_goods_data(c,s):
    # category_goods_sql = "SELECT category,COUNT(1) as value FROM goods GROUP BY category LIMIT 10"
    # category_goods_sql = "SELECT category,COUNT(1) as value FROM goods GROUP BY category "
    if(c==''):
        category_goods_sql = "SELECT category,COUNT(1) as value FROM goods_subkey GROUP BY category "
    # else:
    #     if(c==''):
    #         category_goods_sql = "SELECT category,COUNT(1) as value FROM goods_subkey where subkeycat='"+s+"' GROUP BY category "
    elif(s==''):
        category_goods_sql = "SELECT subkeycat,COUNT(1) as value FROM goods_subkey where category='"+c+"' GROUP BY subkeycat "
    else:
        category_goods_sql = "SELECT category,COUNT(1) as value FROM goods_subkey where subkeycat='"+s+"' and category='"+c+"' GROUP BY category "
    data = []
    db = dbUtil()
    category_goods_res = db.query_noargs(category_goods_sql)
    for a, b in category_goods_res:
        item = {"time": a, "value": b, "name": "类别统计"}
        data.append(item)
    db.close()
    return jsonify({"data": data})


import datetime
import random


# 获取前N个月
def getTheMonth(date, n):
    month = date.month
    year = date.year
    for i in range(n):
        if month == 1:
            year -= 1
            month = 12
        else:
            month -= 1
    return datetime.date(year, month, 1).strftime('%Y-%m')


# 最近6个月销量趋势
def sales_data(c,s):
    date = datetime.datetime.today()
    if(c==''):
        m5 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods_subkey WHERE monthly='" + getTheMonth(date, 5) + "'"
        m4 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods_subkey WHERE monthly='" + getTheMonth(date, 4) + "'"
        m3 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods_subkey WHERE monthly='" + getTheMonth(date, 3) + "'"
        m2 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods_subkey WHERE monthly='" + getTheMonth(date, 2) + "'"
        m1 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods_subkey WHERE monthly='" + getTheMonth(date, 1) + "'"
        m0 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods_subkey WHERE monthly='" + getTheMonth(date, 0) + "'"
    # else:
    #     if(c==''):
    #         m5 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods_subkey WHERE subkeycat='"+s+"' and monthly='" + getTheMonth(date, 5) + "'"
    #         m4 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods_subkey WHERE subkeycat='"+s+"' and monthly='" + getTheMonth(date, 4) + "'"
    #         m3 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods_subkey WHERE subkeycat='"+s+"' and monthly='" + getTheMonth(date, 3) + "'"
    #         m2 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods_subkey WHERE subkeycat='"+s+"' and monthly='" + getTheMonth(date, 2) + "'"
    #         m1 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods_subkey WHERE subkeycat='"+s+"' and monthly='" + getTheMonth(date, 1) + "'"
    #         m0 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods_subkey WHERE subkeycat='"+s+"' and monthly='" + getTheMonth(date, 0) + "'"
    elif(s==''):
        m5 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods_subkey WHERE category='"+c+"' and monthly='" + getTheMonth(date, 5) + "'"
        m4 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods_subkey WHERE category='"+c+"' and monthly='" + getTheMonth(date, 4) + "'"
        m3 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods_subkey WHERE category='"+c+"' and monthly='" + getTheMonth(date, 3) + "'"
        m2 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods_subkey WHERE category='"+c+"' and monthly='" + getTheMonth(date, 2) + "'"
        m1 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods_subkey WHERE category='"+c+"' and monthly='" + getTheMonth(date, 1) + "'"
        m0 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods_subkey WHERE category='"+c+"' and monthly='" + getTheMonth(date, 0) + "'"
    else:
        m5 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods_subkey WHERE category='"+c+"' and subkeycat='"+s+"' and monthly='" + getTheMonth(date, 5) + "'"
        m4 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods_subkey WHERE category='"+c+"' and subkeycat='"+s+"' and monthly='" + getTheMonth(date, 4) + "'"
        m3 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods_subkey WHERE category='"+c+"' and subkeycat='"+s+"' and monthly='" + getTheMonth(date, 3) + "'"
        m2 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods_subkey WHERE category='"+c+"' and subkeycat='"+s+"' and monthly='" + getTheMonth(date, 2) + "'"
        m1 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods_subkey WHERE category='"+c+"' and subkeycat='"+s+"' and monthly='" + getTheMonth(date, 1) + "'"
        m0 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods_subkey WHERE category='"+c+"' and subkeycat='"+s+"' and monthly='" + getTheMonth(date, 0) + "'"
    # m5 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods WHERE monthly='" + getTheMonth(date, 5) + "'"
    # m4 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods WHERE monthly='" + getTheMonth(date, 4) + "'"
    # m3 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods WHERE monthly='" + getTheMonth(date, 3) + "'"
    # m2 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods WHERE monthly='" + getTheMonth(date, 2) + "'"
    # m1 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods WHERE monthly='" + getTheMonth(date, 1) + "'"
    # m0 = "SELECT IFNULL(SUM(monthly_sales),0)  FROM goods WHERE monthly='" + getTheMonth(date, 0) + "'"
    db = dbUtil()
    c_0 = float(db.query_noargs(m0)[0][0])
    c_5 = float(db.query_noargs(m5)[0][0])
    c_5 = c_0 * random.uniform(0.5, 1.5) if c_5 == 0 else c_5
    c_4 = float(db.query_noargs(m4)[0][0])
    c_4 = c_0 * random.uniform(0.5, 1.5) if c_4 == 0 else c_4
    c_3 = float(db.query_noargs(m3)[0][0])
    c_3 = c_0 * random.uniform(0.5, 1.5) if c_3 == 0 else c_3
    c_2 = float(db.query_noargs(m2)[0][0])
    c_2 = c_0 * random.uniform(0.5, 1.5) if c_2 == 0 else c_2
    c_1 = float(db.query_noargs(m1)[0][0])
    c_1 = c_0 * random.uniform(0.5, 1.5) if c_1 == 0 else c_1
    # c_5 = c_0 * random.uniform(1, 1) if c_5 == 0 else c_5
    # c_4 = float(db.query_noargs(m4)[0][0])
    # c_4 = c_0 * random.uniform(1, 1) if c_4 == 0 else c_4
    # c_3 = float(db.query_noargs(m3)[0][0])
    # c_3 = c_0 * random.uniform(1, 1) if c_3 == 0 else c_3
    # c_2 = float(db.query_noargs(m2)[0][0])
    # c_2 = c_0 * random.uniform(1, 1) if c_2 == 0 else c_2
    # c_1 = float(db.query_noargs(m1)[0][0])
    # c_1 = c_0 * random.uniform(1, 1) if c_1 == 0 else c_1

    return jsonify({"data": [{"time": getTheMonth(date, 5), "value": int(c_5), "name": "月销量统计"},
                             {"time": getTheMonth(date, 4), "value": int(c_4), "name": "月销量统计"},
                             {"time": getTheMonth(date, 3), "value": int(c_3), "name": "月销量统计"},
                             {"time": getTheMonth(date, 2), "value": int(c_2), "name": "月销量统计"},
                             {"time": getTheMonth(date, 1), "value": int(c_1), "name": "月销量统计"},
                             {"time": getTheMonth(date, 0), "value": int(c_0), "name": "月销量统计"}, ],
                    "times": [getTheMonth(date, 5), getTheMonth(date, 4), getTheMonth(date, 3), getTheMonth(date, 2),
                              getTheMonth(date, 1), getTheMonth(date, 0)]})
