from flask import Flask as _Flask, flash
from flask import request, session
from flask import render_template
from flask.json import JSONEncoder as _JSONEncoder, jsonify
import decimal
import requests
import service.users_data as user_service
import service.getmaincat as main_service
import service.notice_data as notice_data
import service.slog_data as slog_data
import service.goods_data as goods_data
import service.category_data as category_data
import service.view_data as view_data
import service.version_data as version_data
import machine_learning.goods_predict as gp
import service.getmaincat as gm
from machine_learning import getlist

import service.view_data as main_view_data
from spider import shopping_spider
from concurrent.futures import ThreadPoolExecutor




class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(_JSONEncoder, self).default(o)


class Flask(_Flask):
    json_encoder = JSONEncoder


import os

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)


# -------------前台可视化大数据分析相关服务接口start-----------------
# 系统默认路径前台跳转
@app.route('/')
def main_page():
    return render_template("main.html")




# -------------前台可视化大数据分析相关服务接口end-----------------
@app.route('/main/returndata', methods=['POST'])
def maindata():
    if request.method == 'POST':
        value = request.form.get('value')
        value2 = request.form.get('value2')
        # print(view_data.total_data(value,value2))
        # requests.post("http://127.0.0.1:5001/data/total", data=view_data.total_data(value,value2))
        # total_data(value,value2)
        # sales_top(value,value2)
        # shop_top(value,value2)
        # sales_distribution(value,value2)
        # price_distribution(value,value2)
        # category_data_view(value,value2)
        # sales_data(value,value2)
        print('success')
        # print(value,value2)
        # return total_data(value,value2)
    return "200"
        #totalData=main_view_data.total_data(value,value2)
        #goodsSalesTop=main_view_data.goods_sales_top(value,value2)
        #shopSalesTop=main_view_data.shop_sales_top(value,value2)
        #salesDistributionData=main_view_data.sales_distribution_data(value,value2)
        #priceDistributionData=main_view_data.price_distribution_data(value,value2)
        #categoryGoodsData= main_view_data.category_goods_data(value,value2)
        #salesData =  main_view_data.sales_data(value,value2)
        #print(totalData,goodsSalesTop,shopSalesTop,salesDistributionData,priceDistributionData,categoryGoodsData,salesData)
        # return jsonify({"totalData": totalData, "goodsSalesTop": goodsSalesTop, "shopSalesTop": shopSalesTop, "salesDistributionData": salesDistributionData, "priceDistributionData": priceDistributionData,"categoryGoodsData": categoryGoodsData,"salesData": salesData})

# -------------后台管理模块相关服务接口start-----------------
# 登录
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        account = request.form.get('account')
        password = request.form.get('password')
        if not all([account, password]):
            flash('参数不完整')
            return "300"
        res = user_service.get_user(account, password)
        if res and res[0][0] > 0:
            session['is_login'] = True
            session['role'] = res[0][1]
            return "200"
        else:
            return "300"

# 登录页面跳转
@app.route('/admin')
def admin():
    if session.get("is_login"):
        if session.get('role') == 0:#0为管理员
            return render_template('index.html')
        else:
            return render_template('index1.html')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    try:
        session.pop("is_login")
        return render_template('login.html')
    except Exception:
        return render_template('login.html')

# 后台首页面跳转
@app.route('/html/welcome')
def welcome():
    return render_template('html/welcome.html')

# 后台注册跳转
@app.route('/html/reg')
def html_reg():
    return render_template('reg.html')

# -----------------用户管理模块START-----------------
# 用户管理页面
@app.route('/html/user')
def user_manager():
    return render_template('html/user.html')

# 获取用户数据分页
@app.route('/user/list', methods=["POST"])
def user_list():
    get_data = request.form.to_dict()
    page_size = get_data.get('page_size')
    page_no = get_data.get('page_no')
    param = get_data.get('param')
    data, count, page_list, max_page = user_service.get_user_list(int(page_size), int(page_no), param)
    return jsonify({"data": data, "count": count, "page_no": page_no, "page_list": page_list, "max_page": max_page})


# 注册用户数据
@app.route('/user/reg', methods=["POST"])
def user_reg():
    get_data = request.form.to_dict()
    name = str(get_data.get('username'))
    account = str(get_data.get('account'))
    password = str(get_data.get('password'))
    company = "平台注册"
    phone = " "
    mail = " "
    type = 1
    return user_service.add_user(name, account, password, company, phone, mail, type)


# 添加用户数据
@app.route('/user/add', methods=["POST"])
def user_add():
    get_data = request.form.to_dict()
    name = get_data.get('name')
    account = get_data.get('account')
    password = get_data.get('password')
    company = get_data.get('company')
    phone = get_data.get('phone')
    mail = get_data.get('mail')
    type = get_data.get('type')
    return user_service.add_user(name, account, password, company, phone, mail, type)


# 修改用户数据
@app.route('/user/edit', methods=["PUT"])
def user_edit():
    get_data = request.form.to_dict()
    id = get_data.get('id')
    name = get_data.get('name')
    password = get_data.get('password')
    company = get_data.get('company')
    phone = get_data.get('phone')
    mail = get_data.get('mail')
    type = get_data.get('type')
    user_service.edit_user(id, name, password, company, phone, mail, type)
    return '200'


# 删除用户数据
@app.route('/user/delete', methods=["DELETE"])
def user_delete():
    get_data = request.form.to_dict()
    id = get_data.get('id')
    user_service.del_user(id)
    return '200'


# -----------------用户管理模块END-----------------


# -----------------公告管理模块START-----------------

# 公告管理页面
@app.route('/html/notice')
def notice_manager():
    return render_template('html/notice.html')


# 获取最新公告
@app.route('/notice/new', methods=["POST"])
def notice_new():
    res = notice_data.get_notice()
    return jsonify({"title": res[1], "content": res[2], "user_name": res[3], "create_time": str(res[4])})


# 获取公告数据分页
@app.route('/notice/list', methods=["POST"])
def notice_list():
    get_data = request.form.to_dict()
    page_size = get_data.get('page_size')
    page_no = get_data.get('page_no')
    param = get_data.get('param')
    data, count, page_list, max_page = notice_data.get_notice_list(int(page_size), int(page_no), param)
    return jsonify({"data": data, "count": count, "page_no": page_no, "page_list": page_list, "max_page": max_page})


# 新增公告数据
@app.route('/notice/add', methods=["POST"])
def notice_add():
    get_data = request.form.to_dict()
    title = get_data.get('title')
    content = get_data.get('content')
    user_name = get_data.get('user_name')
    return notice_data.add_notice(title, content, user_name)


# 修改公告数据
@app.route('/notice/edit', methods=["PUT"])
def notice_edit():
    get_data = request.form.to_dict()
    id = get_data.get('id')
    title = get_data.get('title')
    content = get_data.get('content')
    user_name = get_data.get('user_name')
    notice_data.edit_notice(id, title, content, user_name)
    return '200'


# 删除公告数据
@app.route('/notice/delete', methods=["DELETE"])
def notice_delete():
    get_data = request.form.to_dict()
    id = get_data.get('id')
    notice_data.del_notice(id)
    return '200'


# -----------------公告管理模块END-----------------


# -----------------系统版本管理模块START-----------------

# 系统版本管理页面
@app.route('/html/version')
def version_manager():
    return render_template('html/version.html')


@app.route('/main/data')
def main_page2():
    res = main_service.get_maincat()
    return jsonify({"data":res})


# 获取系统版本
@app.route('/version/show', methods=["POST"])
def version_show():
    res = version_data.get_sys_version()
    return jsonify({"data": res})


# 获取系统版本数据分页
@app.route('/version/list', methods=["POST"])
def version_list():
    get_data = request.form.to_dict()
    page_size = get_data.get('page_size')
    page_no = get_data.get('page_no')
    param = get_data.get('param')
    data, count, page_list, max_page = version_data.get_sys_version_list(int(page_size), int(page_no), param)
    return jsonify({"data": data, "count": count, "page_no": page_no, "page_list": page_list, "max_page": max_page})


# 新增系统版本数据
@app.route('/version/add', methods=["POST"])
def sys_version_add():
    get_data = request.form.to_dict()
    name = get_data.get('name')
    version = get_data.get('version')
    return version_data.add_sys_version(name, version)


# 修改系统版本数据
@app.route('/version/edit', methods=["PUT"])
def version_edit():
    get_data = request.form.to_dict()
    id = get_data.get('id')
    name = get_data.get('name')
    version = get_data.get('version')
    version_data.edit_sys_version(id, name, version)
    return '200'


# 删除系统版本数据
@app.route('/version/delete', methods=["DELETE"])
def version_delete():
    get_data = request.form.to_dict()
    id = get_data.get('id')
    version_data.del_sys_version(id)
    return '200'


# -----------------系统版本管理模块END-----------------

# -----------------类别管理模块START-----------------

# 公告管理页面
@app.route('/html/category')
def category_manager():
    if(session.get('role')==0):
        return render_template('html/category.html')
    else:
        return render_template('html/category1.html')


# 获取公告数据分页
@app.route('/category/list', methods=["POST"])
def category_list():
    get_data = request.form.to_dict()
    page_size = get_data.get('page_size')
    page_no = get_data.get('page_no')
    param = get_data.get('param')
    data, count, page_list, max_page = category_data.get_category_list(int(page_size), int(page_no), param)
    return jsonify({"data": data, "count": count, "page_no": page_no, "page_list": page_list, "max_page": max_page})


# 新增类别数据
# @app.route('/category/add', methods=["POST"])
# def category_add():
#     get_data = request.form.to_dict()
#     content = get_data.get('content')
#     return category_data.add_category(content)
@app.route('/category/add', methods=["POST"])
def category_add():
    if(session.get('role')==0):
        get_data = request.form.to_dict()
        content = get_data.get('content')
    return category_data.add_category(content)

# 修改类别数据
# @app.route('/category/edit', methods=["PUT"])
# def category_edit():
#     get_data = request.form.to_dict()
#     id = get_data.get('id')
#     content = get_data.get('content')
#     category_data.edit_category(id, content)
#     return '200'
@app.route('/category/edit', methods=["PUT"])
def category_edit():
    if(session.get('role')==0):
        get_data = request.form.to_dict()
        id = get_data.get('id')
        content = get_data.get('content')
        category_data.edit_category(id, content)
    return '200'


# 删除类别数据
# @app.route('/category/delete', methods=["DELETE"])
# def category_delete():
#     get_data = request.form.to_dict()
#     id = get_data.get('id')
#     category_data.del_category(id)
#     return '200'
@app.route('/category/delete', methods=["DELETE"])
def category_delete():
    if(session.get('role')==0):
        get_data = request.form.to_dict()
        id = get_data.get('id')
        category_data.del_category(id)
    return '200'


# -----------------类别管理模块END-----------------

# -----------------爬虫管理模块START-----------------
# 后台调用爬虫
@app.route('/spider/start', methods=["POST"])
def run_spider():
    get_data = request.form.to_dict()
    key = get_data.get('key')
    subkey = get_data.get('subkey')
    total_pages = get_data.get('num')
    executor = ThreadPoolExecutor(2)
    executor.submit(shopping_spider.main(key, subkey, total_pages))
    return '200'


# 爬虫日志页面
@app.route('/html/slog')
def slog_manager():
    return render_template('html/slog.html')


# 获取爬虫日志数据分页
@app.route('/slog/list', methods=["POST"])
def slog_list():
    get_data = request.form.to_dict()
    page_size = get_data.get('page_size')
    page_no = get_data.get('page_no')
    param = get_data.get('param')
    data, count, page_list, max_page = slog_data.get_slog_list(int(page_size), int(page_no), param)
    return jsonify({"data": data, "count": count, "page_no": page_no, "page_list": page_list, "max_page": max_page})


# 修改爬虫日志数据
@app.route('/slog/edit', methods=["PUT"])
def slog_edit():
    get_data = request.form.to_dict()
    id = get_data.get('id')
    log = get_data.get('log')
    slog_data.edit_slog(id, log)
    return '200'


# 删除爬虫日志数据
@app.route('/slog/delete', methods=["DELETE"])
def slog_delete():
    get_data = request.form.to_dict()
    id = get_data.get('id')
    slog_data.del_slog(id)
    return '200'


# -----------------爬虫管理模块END-----------------


# -----------------商品管理模块START----------------
# 商品页面
# @app.route('/html/goods')
# def goods_manager():
#     return render_template('html/goods.html')
@app.route('/html/goods')
def goods_manager():
    if(session.get('role')==0):
        return render_template('html/goods.html')
    else:
        return render_template('html/goods1.html')

# 获取商品数据分页
@app.route('/goods/list', methods=["POST"])
def goods_list():
    get_data = request.form.to_dict()
    page_size = get_data.get('page_size')
    page_no = get_data.get('page_no')
    param = get_data.get('param')
    data, count, page_list, max_page = goods_data.get_goods_list(int(page_size), int(page_no), param)
    return jsonify({"data": data, "count": count, "page_no": page_no, "page_list": page_list, "max_page": max_page})


# 修改商品数据     if(session.get('role')==0):
# @app.route('/goods/edit', methods=["PUT"])
# def goods_edit():
#     get_data = request.form.to_dict()
#     id = get_data.get('id')
#     title = get_data.get('title')
#     category = get_data.get('category')
#     discount = get_data.get('discount')
#     original_price = get_data.get('original_price')
#     shop = get_data.get('shop')
#     monthly_sales = get_data.get('monthly_sales')
#     goods_data.edit_goods(id, title, category, discount, original_price, shop, monthly_sales)
#     return '200'
@app.route('/goods/edit', methods=["PUT"])
def goods_edit():
    if(session.get('role')==0):
        get_data = request.form.to_dict()
        id = get_data.get('id')
        title = get_data.get('title')
        category = get_data.get('category')
        discount = get_data.get('discount')
        original_price = get_data.get('original_price')
        shop = get_data.get('shop')
        monthly_sales = get_data.get('monthly_sales')
        goods_data.edit_goods(id, title, category, discount, original_price, shop, monthly_sales)
    return '200'


# 删除商品数据 if(session.get('role')==0):
# @app.route('/goods/delete', methods=["DELETE"])
# def goods_delete():
#     get_data = request.form.to_dict()
#     id = get_data.get('id')
#     goods_data.del_goods(id)
#     return '200'
@app.route('/goods/delete', methods=["DELETE"])
def goods_delete():
    if(session.get('role')==0):
        get_data = request.form.to_dict()
        id = get_data.get('id')
        goods_data.del_goods(id)
    return '200'


# 预测页面
@app.route('/html/predict')
def html_predict():
    return render_template('html/predict.html')


# 预测商品数据
@app.route('/goods/predict', methods=["POST"])
def goods_predict():
    get_data = request.form.to_dict()
    t = get_data.get('t')
    p = get_data.get('p')
    op = get_data.get('op')
    le = get_data.get('le')
    # print(t,p,op,le)
    return jsonify({"data": gp.predict(t, p, op,le)})


# -----------------商品管理模块END-----------------
# -----------------可视化页面模块START-----------------
# 获取页面总计数据
@app.route('/data/total',methods=["POST","GET"])
def total_data(c='',s=''):
    if request.method == 'POST':
        get_data = request.form.to_dict()
        c = get_data.get('c')
        s = get_data.get('s')
        return view_data.total_data(c,s)
    return view_data.total_data(c,s)
# @app.route('/amin/total')
# def total_data1(c,s):
#     print('value:',c,'value2:',s)
#     return view_data.total_data(c,s)

# 商品销量top10
@app.route('/data/sales/top',methods=["POST","GET"])
def sales_top(c='',s=''):
    if request.method == 'POST':
        get_data = request.form.to_dict()
        c = get_data.get('c')
        s = get_data.get('s')
        return view_data.goods_sales_top(c,s)
    return view_data.goods_sales_top(c,s)


# 商铺销量top10
@app.route('/data/shop/top',methods=["POST","GET"])
def shop_top(c='',s=''):
    if request.method == 'POST':
        get_data = request.form.to_dict()
        c = get_data.get('c')
        s = get_data.get('s')
        return view_data.shop_sales_top(c,s)
    return view_data.shop_sales_top(c,s)


# 销量分布
@app.route('/data/sales/distribution',methods=["POST","GET"])
def sales_distribution(c='',s=''):
    if request.method == 'POST':
        get_data = request.form.to_dict()
        c = get_data.get('c')
        s = get_data.get('s')
        return view_data.sales_distribution_data(c,s)
    return view_data.sales_distribution_data(c,s)


# 价格分布
@app.route('/data/price/distribution',methods=["POST","GET"])
def price_distribution(c='',s=''):
    if request.method == 'POST':
        get_data = request.form.to_dict()
        c = get_data.get('c')
        s = get_data.get('s')
        return view_data.price_distribution_data(c,s)
    return view_data.price_distribution_data(c,s)


# 类别统计
@app.route('/data/category/count',methods=["POST","GET"])
def category_data_view(c='',s=''):
    if request.method == 'POST':
        get_data = request.form.to_dict()
        c = get_data.get('c')
        s = get_data.get('s')
        return view_data.category_goods_data(c,s)
    return view_data.category_goods_data(c,s)


# 最近6个月销量趋势
@app.route('/data/sales/month',methods=["POST","GET"])
def sales_data(c='',s=''):
    if request.method == 'POST':
        get_data = request.form.to_dict()
        c = get_data.get('c')
        s = get_data.get('s')
        return view_data.sales_data(c,s)
    return view_data.sales_data(c,s)

@app.route('/data/select')
def select_category():
    return gm.get_maincat()

# -----------------可视化页面模块END-----------------
if __name__ == '__main__':
    # 端口号设置
    app.run(host="127.0.0.1", port=5000)
