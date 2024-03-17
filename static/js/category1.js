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



    // 类别编辑
    window.category_edit = function (title, a, b) {
        w = '520px'
        he = '220px'
        $('#id').val(a);
        $('#content').val(b);
        layer.open({
            type: 1,
            area: [w, he],
            fix: false, //不固定
            maxmin: true,
            shadeClose: true,
            shade: 0.4,
            title: title,
            content: $('#category-form')
        });
    }


});
get_category_data(page_no);
max_page = 0;

function get_category_data(no) {
    page_no = no;
    $.ajax({
        url: "/category/list",
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
            '<td>' + item[1] + '</td>'
    }
    if (page_no == 1) {
        page_str = ''
    } else {
        page_str = '<span class="prev" onclick="get_category_data(' + (page_no - 1) + ')">&lt;&lt;</span>';
    }
    page_str = '<span>共' + page + '页，' + count + '条数据</span>' + page_str
    for (var i = 0; i < page_list.length; i++) {
        item = page_list[i];
        if (item == page_no) {
            page_str = page_str + '<span class="current">' + item + '</span>'
        } else {
            page_str = page_str + '<span class="num" onclick="get_category_data(' + item + ')">' + item + '</span>'
        }
    }
    if (page_no != max_page) {
        page_str = page_str + ' <span class="next" onclick="get_category_data(' + (page_no + 1) + ')">&gt;&gt;</span>'
    }
    $("#category_data").html(list_data);
    $("#page_list").html(page_str);

}



/*查询*/
function get_search() {
    param = ' 1=1 ';
    content_s = $("#content_s").val();
    if (content_s != null && content_s != '') {
        param = param + " and content LIKE '%%" + content_s + "%%'";
    }

    all_page_param = param;
    get_category_data(page_no)
}