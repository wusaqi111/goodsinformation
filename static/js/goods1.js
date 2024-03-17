page_no = 1;
all_page_param = ' 1=1 ';
layui.use(['form', 'layer', 'laydate'], function () {

    $ = layui.jquery;
    var form = layui.form,
        layer = layui.layer,
        laydate = layui.laydate;
    //执行一个laydate实例
    laydate.render({
        elem: '#start' //指定元素
    });

    //执行一个laydate实例
    laydate.render({
        elem: '#end' //指定元素
    });
});
get_goods_data(page_no);
max_page = 0;

function get_goods_data(no) {
    page_no = no;
    $.ajax({
        url: "/goods/list",
        data: {"page_size": 10, "page_no": page_no, "param": all_page_param},
        method: "POST",
        success: function (obj) {
            page_data = obj.data;
            page_list = obj.page_list;
            max_page = obj.max_page;
            count = obj.count;
            show_data(page_data, page_no, page_list, count, max_page)
        },
        error: function (xhr, type, errorThrown) {

        }
    })
}

function show_data(page_data, page_no, page_list, count, page) {
    list_data = '';
    for (var i = 0; i < page_data.length; i++) {
        item = page_data[i];
        list_data = list_data + '<tr>' +
            '<td>' + (i + 1) + '</td>' +
            '<td>' + item[1] + '</td>' +
            '<td>' + item[2] + '</td>' +
            '<td>' + item[3] + '</td>' +
            '<td>' + item[4] + '</td>' +
            '<td>' + item[5] + '</td>' +
            '<td>' + item[6] + '</td>' +
            '<td>' + item[7] + '</td>' +
            '<td>' + item[8] + '</td>'
        // '<td class="td-manage">' +
        // ' <a title="编辑"  onclick="goods_edit(\'编辑\',' + item[0] + ',\'' + item[1] + '\',\'' + item[2] + '\',\'' + item[3] +'\',\'' + item[4] +'\',\'' + item[5] +'\',\'' + item[6] +'\',\'' + item[7] + '\')" href = "javascript:;" > ' +
        // '  <i class="layui-icon">&#xe63c;</i>' +
        // '  </a>' +
        // '        <a title="删除" onclick="member_del(this,\'' + item[0] + '\')" href="javascript:;">' +
        // '  <i class="layui-icon">&#xe640;</i>' +
        // '              </a>' +
        // '            </td>' +
        // '          </tr>'
    }
    if (page_no == 1) {
        page_str = ''
    } else {
        page_str = '<span class="prev" onclick="get_goods_data(' + (page_no - 1) + ')">&lt;&lt;</span>';
    }
    page_str = '<span>共' + page + '页，' + count + '条数据</span>' + page_str
    for (var i = 0; i < page_list.length; i++) {
        item = page_list[i];
        if (item == page_no) {
            page_str = page_str + '<span class="current">' + item + '</span>'
        } else {
            page_str = page_str + '<span class="num" onclick="get_goods_data(' + item + ')">' + item + '</span>'
        }
    }
    if (page_no != max_page) {
        page_str = page_str + ' <span class="next" onclick="get_goods_data(' + (page_no + 1) + ')">&gt;&gt;</span>'
    }
    $("#goods_data").html(list_data);
    $("#page_list").html(page_str);

}

/*查询*/
function get_search() {
    param = ' 1=1 ';
    title_s = $("#title_s").val();
    shop_s = $("#shop_s").val();
    category_s = $("#category_s").val();
    subkeycat_s = $("#subkeycat_s").val();

    if (title_s != null && title_s != '') {
        param = param + " and title LIKE '%%" + title_s + "%%'";
    }
    if (shop_s != null && shop_s != '') {
        param = param + " and shop LIKE '%%" + shop_s + "%%'";
    }
    if (subkeycat_s != null && subkeycat_s != '') {
        param = param + " and subkeycat LIKE '%%" + subkeycat_s + "%%'";
    }
    if (category_s != null && category_s != '') {
        param = param + " and category LIKE '%%" + category_s + "%%'";
    }
    all_page_param = param;
    get_goods_data(page_no)
}