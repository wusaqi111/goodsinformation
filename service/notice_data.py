from utils import dbUtil
import datetime


# 最新公告业务
def get_notice():
    db = dbUtil()
    sql = "select * from notice order by create_time desc limit 1"
    res = db.query(sql)
    return res[0]


# 公告新增业务
def add_notice(title, content, user_name):
    db = dbUtil()
    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "insert into notice VALUES (NULL, '" + title + "', '" + content + "', '" + user_name + "','" + t + "')"
    db.query(sql)
    db.close()
    return "200"


# 获取公告分页数据
def get_notice_list(page_size, page_no, param):
    db = dbUtil()
    param = param.replace("\\", "")
    count_sql = "select count(*) from notice where " + param
    count_res = db.query(count_sql)[0][0]
    start = page_size * (page_no - 1)
    start = 0 if start < 0 else start
    sql = "select * from  notice where" + param + "order by create_time desc limit " + str(start) + "," + str(page_size)
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
    for a, b, c, d, e in res:
        item = [a, b, c, d, str(e)]
        data_page.append(item)
    db.close()
    return data_page, count_res, page_list, max_page


# 修改公告信息
def edit_notice(id, title, content, user_name):
    db = dbUtil()
    sql = "update  `notice` set title = '" + title + "',content='" + content + "',user_name='" + user_name + "' where id=" + id
    res = db.query(sql)
    db.close()
    return res


# 删除公告信息
def del_notice(id):
    db = dbUtil()
    sql = "delete from  `notice` where id=" + id
    res = db.query(sql)
    db.close()
    return res
