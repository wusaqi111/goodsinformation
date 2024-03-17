page_no = 1;
all_page_param = ' 1=1 ';
layui.use(['form', 'layer', 'laydate'], function () {

    $ = layui.jquery;
    var  layer = layui.layer;

    //预测数据
    window.predict = function () {
        let t = $("#test2").val();
        let p = $("#p").val();
        let op = $("#op").val();
        let le = $("#le").val();
        if (t == undefined || t == "") {
            return layer.msg("请选择商品类别！")
        }
        if (p == undefined || p < 1) {
            return layer.msg("请输入商品折扣价！")
        }
        if (le == undefined || le < 1 || le>33) {
            return layer.msg("店铺销售能力输入错误！")
        }
        if (op == undefined || op < 1) {
            return layer.msg("请输入商品原价！")
        }
        let index = layer.load();
        $.ajax({
            url: "/goods/predict",
            method: "POST",
            data: {"t": t, "p": p, "op": op,"le":le},
            success: function (obj) {
                layer.close(index);
                $("#predict").html(obj.data)
                layer.msg("预测成功！", {icon: 6})
            },
            error: function (xhr, type, errorThrown) {
            }
        });
    }

});