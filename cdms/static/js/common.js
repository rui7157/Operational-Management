(function ($) {
    $.fn.livedemo = function (options) {

        var codeblock = $('<div class="code-block"></div>');
        var blockclose = $('<span class="block-close">x</span>');

        return this.each(function () {

            var livedemo = $(this);

            livedemo.on('click', '.btn-code', function (e) {
                e.preventDefault();

                var btn = $(this);
                var block = $(this).parents('.demo-block');
                var codes = block.find('.demo-code').html();

                if (block.next().hasClass('code-block')) {
                    block.next().stop().slideToggle();
                } else {
                    livedemo.find('.btn-code').removeClass('filled');
                    livedemo.find('.code-block').stop().slideUp(function () {
                        $(this).remove()
                    });

                    var newblock = codeblock.clone();
                    newblock.append(codes).append(blockclose).insertAfter(block).slideDown();
                }

                $(this).toggleClass('filled');

            }).on('click', '.block-close', function () {
                $(this).parents('.code-block').stop().slideUp().prev('.demo-block').find('.btn-code').removeClass('filled');
            });

        });

    };
})(jQuery);

function date_count(bng, end) {
    //时间计算函数

    var bngDate = new Date(bng.substr(0, 4), bng.substr(5, 2), bng.substr(8, 2));
    var endDate = new Date(end.substr(0, 4), end.substr(5, 2) - 1, end.substr(8, 2));
    var days = (endDate.getTime() - bngDate.getTime()) / 24 / 60 / 60 / 1000;
    return days;
}

function formatDate(date, format) {
    //日期格式化
    if (!date) return;
    if (!format) format = "yyyy-MM-dd";
    switch (typeof date) {
        case "string":
            date = new Date(Date.parse(date.replace(/-/g, "/")));
            break;
        case "number":
            date = new Date(date);
            break;
    }
    if (!date instanceof Date) return;
    var dict = {
        "yyyy": date.getFullYear(),
        "M": date.getMonth() + 1,
        "d": date.getDate(),
        "H": date.getHours(),
        "m": date.getMinutes(),
        "s": date.getSeconds(),
        "MM": ("" + (date.getMonth() + 101)).substr(1),
        "dd": ("" + (date.getDate() + 100)).substr(1),
        "HH": ("" + (date.getHours() + 100)).substr(1),
        "mm": ("" + (date.getMinutes() + 100)).substr(1),
        "ss": ("" + (date.getSeconds() + 100)).substr(1)
    };
    return format.replace(/(yyyy|MM?|dd?|HH?|ss?|mm?)/g, function () {
        return dict[arguments[0]];
    });
}


$(function () {
    //展开菜单
    $('#menu').tendina({
        openCallback: function (clickedEl) {
            clickedEl.addClass('opened');
        },
        closeCallback: function (clickedEl) {
            clickedEl.addClass('closed');
        }
    });

    $("#ad_setting").click(function () {
        $("#ad_setting_ul").slideDown("fast");
    });
    ($("#ad_setting_ul"), $("#ad_setting")).mouseleave(function () {
        $("#ad_setting_ul").slideUp("fast");
    });
    $("#ad_setting_ul li").mouseenter(function () {
        $(this).find("a").attr("class", "ad_setting_ul_li_a");
    });
    $("#ad_setting_ul li").mouseleave(function () {
        $(this).find("a").attr("class", "");
    });


    //检验输入框
    $("#check_pwd2").blur(function () {
        if ($("#check_pwd1").val() != $(this).val()) {
            new $.flavr('两次输入密码不一致！');
            $("#ok_btn").attr("class", "btn disabled");
        } else {
            if ($("#check_pwd1").val() == "") {
                new $.flavr('输入密码不能为空！');
                $("#ok_btn").attr("class", "btn disabled");
            } else {
                $("#ok_btn").attr("class", "btn");
            }
        }
    });

    //时间选择

    $('.datetimepicker').datetimepicker({
        minView: "month", //选择日期后，不会再跳转去选择时分秒
        format: "yyyy-mm-dd", //选择日期后，文本框显示的日期格式
        language: 'zh-CN', //汉化
        todayBtn: true,
        autoclose: true //选择日期后自动关闭
    });


    for (var i = 1; i < $("#server tr").length; i++) {
        var date = $($($("#server tr")[i]).children()[11]).text();
        var d = new Date();
        var current_date = formatDate(d.getFullYear() + "-" + d.getMonth() + "-" + d.getDate(), "yyyy-MM-dd");
        var rem_day = date_count(current_date, date.replace(/(^\s*)|(\s*$)/g, ''));
        if (rem_day < 3) {
            $($("#server tr")[i]).addClass("danger");
        } else if (rem_day < 7) {
            $($("#server tr")[i]).addClass("warning");
        } else {
            $($("#server tr")[i]).addClass("active");
        }
        ;
    }


    //找到所有名字的单元格
    var name = $("#tbody td:even");
    //给这些单元格注册鼠标点击事件
    $("#tbody td").click(function () {
        var currentTr = $(this).parent();
        if ($(this).has("a").length > 0) {
            return false;
        } else {
            //找到当前鼠标单击的td
            var tdObj = $(this);
            //保存原来的文本
            var oldText = $(this).text();
            //创建一个文本框
            var inputObj = $("<input type='text' value='" + oldText + "'/>");
            //去掉文本框的边框
            inputObj.css("border-width", 0);
            inputObj.click(function () {
                return false;
            });
            //使文本框的宽度和td的宽度相同
            inputObj.width(tdObj.width());
            inputObj.height(tdObj.height());
            //去掉文本框的外边距
            inputObj.css("margin", 0);
            inputObj.css("padding", 0);
            inputObj.css("text-align", "center");
            inputObj.css("font-size", "16px");
            inputObj.css("background-color", tdObj.css("background-color"));
            //把文本框放到td中
            tdObj.html(inputObj);
            //文本框失去焦点的时候变为文本
            inputObj.blur(function () {
                var newText = $(this).val();
                tdObj.html(newText);
                var trSid = tdObj.parent().attr("sid");
                var tdText = tdObj.parent().children();
                data = {
                    "sid": trSid,
                    "application": tdText[0].innerText,
                    "server_name": tdText[1].innerText,
                    "server_account": tdText[2].innerText,
                    "server_password": tdText[3].innerText,
                    "server_ip": tdText[4].innerText,
                    "server_lan_ip": tdText[5].innerText,
                    "root_auth": tdText[6].innerText,
                    "login_path": tdText[7].innerText,
                    "ftp_auth": tdText[8].innerText,
                    "ip_ext": tdText[9].innerText,
                    "price": tdText[10].innerText,
                    "start_time": tdText[11].innerText,
                    "end_time": tdText[12].innerText
                };
                $.post("/admin/modify_server", data, function (sulth) {
                    if (sulth == "fail") {
                        alert("修改失败");
                    }
                });
            });
            //全选
            inputObj.trigger("focus").trigger("select");
        }
    });


    //服务器删除
    $(".delbtn").click(function () {
        var sid = $(this).parent().parent().attr("sid");
        var current_tr = $(this).parent().parent();
        $.post("/admin/delete_server", {"sid": sid}, function (result) {
            if (result == "success") {
                current_tr.hide("slow");
            } else {
                alert("删除失败!")
            }
        });
    });

    //添加site跳转
    $(".add_application").click(function () {
        var sid = $(this).parent().parent().attr("sid");
        top.location = 'add_application?&sid=' + sid;
    });  //return false;
    $("#add_application").click(function () {
        $("#add_site tbody").append("<tr><td style='display: none'><input name='sid' value=" + $('sid').attr('sid') + "></td><td><input name='ip' placeholder='输入数据'></td><td><input name='name' placeholder='输入数据'></td><td><input name='domain' placeholder='输入数据'></td><td><input name='other' placeholder='输入数据'></td><td><button class='table_btn add_save'>保存</button></td></tr>");
        $("#add_site tbody input").css("width", "100%");
        $("#add_site tbody input").css("height", "100%");
    });

    $(".del_site").click(function () {
        var current_tr = $(this).parent().parent();
        $.post("delete_site", {"wid": $(this).attr("wid")}, function (result) {
            if (result == "success") {

                current_tr.hide("slow");
            }
        })

    });

    $("#query_server tr").dblclick(function(){
        var sid=$(this).attr("sid");
        window.open('query_site?&sid='+sid,'newwindow','height=500,width=720, top=300,left=500,toolbar=no,menubar=no,scrollbars=yes, resizable=no,location=no, status=no');
    });
});
