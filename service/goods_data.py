from utils import dbUtil


# 获取商品数据分页数据
def get_goods_list(page_size, page_no, param):
    db = dbUtil()
    param = param.replace("\\", "")
    count_sql = "select count(*) from goods_subkey where " + param
    count_res = db.query(count_sql)[0][0]
    start = page_size * (page_no - 1)
    start = 0 if start < 0 else start
    # sql = "select * from  goods_subkey where" + param + "order by id desc limit " + str(start) + "," + str(page_size)
    sql = "select id,title,category,subkeycat,discount,original_price,shop,monthly_sales,monthly from  goods_subkey where" + param + "order by id desc limit " + str(start) + "," + str(page_size)
    res = db.query(sql)
    data_page = []
    if count_res % page_size == 0:
        max_page = int(count_res / page_size)
    else:
        max_page = int(count_res / page_size) + 1
    if max_page <= 5:
        page_list = [i for i in range(1, max_page + 1, 1)]
    elif page_no + 2 > max_page:
        page_list = [i for i in range(max_page - 5, max_page + 1, 1)]
    elif page_no - 2 < 1:
        page_list = [i for i in range(1, 6, 1)]
    else:
        page_list = [i for i in range(page_no - 2, page_no + 3, 1)]
    for a, b, c, d, e, f, g, h,j in res:
        item = [a, b, c, d, e, f, g, h,j]
        data_page.append(item)
    db.close()
    return data_page, count_res, page_list, max_page


# 修改商品数据信息
def edit_goods(id, title, category, discount, original_price, shop, monthly_sales):
    db = dbUtil()
    sql = "update  `goods` set title = '" + title + "',category = '" + category + "',discount = " + discount + ",original_price = " + original_price + ",shop = '" + shop + "',monthly_sales = " + monthly_sales + " where id=" + id
    res = db.query(sql)
    db.close()
    return res


# 删除商品数据信息
def del_goods(id):
    db = dbUtil()
    sql = "delete from  `goods` where id=" + id
    res = db.query(sql)
    db.close()
    return res
