from utils import dbUtil


# 类别新增业务
def add_category(content):
    db = dbUtil()
    sql = "insert into category VALUES (NULL,  '" + content + "')"
    db.query(sql)
    db.close()
    return "200"


# 获取类别分页数据
def get_category_list(page_size, page_no, param):
    db = dbUtil()
    param = param.replace("\\", "")
    count_sql = "select count(*) from category where " + param
    count_res = db.query(count_sql)[0][0]
    start = page_size * (page_no - 1)
    start = 0 if start < 0 else start
    sql = "select * from  category where" + param + "order by id desc limit " + str(start) + "," + str(
        page_size)
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
    for a, b, in res:
        item = [a, b]
        data_page.append(item)
    db.close()
    return data_page, count_res, page_list, max_page


# 修改类别信息
def edit_category(id, content):
    db = dbUtil()
    sql = "update  `category` set content='" + content + "' where id=" + id
    res = db.query(sql)
    db.close()
    return res


# 删除类别信息
def del_category(id):
    db = dbUtil()
    sql = "delete from  `category` where id=" + id
    res = db.query(sql)
    db.close()
    return res
