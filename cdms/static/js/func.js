/**
 * Created by bayonet on 16-3-6.
 */



/* loading 特效 */
var CommonPerson = {};
CommonPerson.Base = {};
CommonPerson.Base.LoadingPic = {
    operation: {
        timeTest: null,                     //延时器
        loadingCount: 0,                    //计数器 当同时被多次调用的时候 记录次数
        loadingImgUrl: "{{ url_for('static', filename='images/loading.gif' ) }}",  //默认load图地址
        loadingImgHeight: 24,               //Loading图的高
        loadingImgWidth: 24                 //Loading图的宽
    },

    //显示全屏Loading图
    FullScreenShow: function (msg) {
        if (msg === undefined) {
            msg = "<img src='../static/images/loading.gif' width='24px' height='24px'/>数据加载中, 请稍等...";
        }

        if ($("#div_loadingImg").length == 0) {
            $("body").append("<div id='div_loadingImg'></div>");
        }
        if (this.operation.loadingCount < 1) {
            this.operation.timeTest = setTimeout(function () {
                $("#div_loadingImg").append("<div id='loadingPage_bg' class='loadingPage_bg1'></div><div id='loadingPage'>" + msg + "</div>");
                $("#loadingPage_bg").height($(top.window.document).height()).width($(top.window.document).width());
            }, 100);
        }
        this.operation.loadingCount += 1;
    },

    //隐藏全屏Loading图
    FullScreenHide: function () {
        this.operation.loadingCount -= 1;
        if (this.operation.loadingCount <= 0) {
            clearTimeout(this.operation.timeTest);
            $("#div_loadingImg").empty();
            $("#div_loadingImg").remove();
            this.operation.loadingCount = 0;
        }
    }

};


$(document).ready(function () {
//$(".nav li").first().addClass("on");
    $(".nav li").click(function () {
        $(this).addClass("on").siblings().removeClass("on")
    });
// 初始化日期

    var myDate = new Date();
    $("[name=idYear] option[value=" + myDate.getFullYear() + "]").attr("selected", true);
    $("[name=idMonth] option[value=" + (1 + myDate.getMonth()) + "]").attr("selected", true);
    $("[name=idDay] option[value=" + myDate.getDate() + "]").attr("selected", true);


});

function ShowElement(element) {
    //双击变为input
    if ($(element).children().prop("tagName") != "INPUT") { //如果已经添加input元素则跳过再次添加
        if ($(element).attr("class") == "modify-btn") {
            $(element).parent().children().find("#post_btn").css("display", "");
        }
        var oldhtml = element.innerHTML;
        var newobj = document.createElement('input');//创建新的input元素

        newobj.type = 'text';//为新增元素添加类型
        newobj.onblur = function () {
            element.innerHTML = this.value ? this.value : oldhtml;//当触发时判断新增元素值是否为空，为空则不修改，并返回原有值
        };
        element.innerHTML = '';
        element.appendChild(newobj);
        newobj.focus();
        newobj.value = oldhtml;
    }
}

$(function () {
    //调用双击事件
    var tds = $("#oTable tr td");
    tds.dblclick(function () {
        ShowElement(this);
    });

    var webrregister = $("#oTable .modify-btn");
    tds.dblclick(function () {
        ShowElement(this);
    })
});

$(function () {
    //保存时候写入数据库
    var post_btn = $(".post-btn");
    post_btn.click(function () {
        //网站地址 	网站用户名 	网站登录密码
        var post_content = $(this).parent().parent().children();
        var periphery_entend_id = $(this).attr("name");
        $.post("/register_web_info_set", {
            "register_website": post_content[0].innerHTML,
            "register_website_username": post_content[1].innerHTML,
            "register_website_password": post_content[2].innerHTML,
            "periphery_entend_id": periphery_entend_id
        }, function (data) {
            if (data) {
                alert("修改成功！")
            }
        });
    });
});


$(function () {
    //菜单滑动效果
    var menu_ul = $("#li>ul"); //父对象
    var menu_li = $("#li>ul>li");
    var menu_li_a = $("#li>ul>li>a");

    menu_ul.append("<li class='slide-li'></li>");  //添加滑动对象li标签
    var slide_li = menu_ul.children(".slide-li");  // 滑动对象
    for (i = 0; i < menu_li_a.length; i++) {              //遍历每一个带 a 标签的菜单项
        var link = menu_li_a.eq(i).attr("href");    //得到第i个a标签的url
        var d_link = document.URL;                   //当前页面的url
        if (d_link.indexOf(link) != -1) {     //     //当前页面是第i个页面
            menu_li.eq(i).addClass("li-active").siblings().removeClass("li-active"); //给第i个页面增加li-active类(特效)
        }
    }
    var on_li = menu_ul.find(".li-active");        //选择停留的对象
    slide_li.css("left", String(on_li.position().left) + "px").css("width", String(on_li.width() - 1 + "px"));   //初始化

    function Slide(li_obj) {
        var li_l = li_obj.position().left;
        var li_w = li_obj.width();
        slide_li.animate({left: li_l, width: li_w - 1}, {queue: false, duration: 200});  //滑动特效宽和左边距移动
    };
    menu_li.hover(function () {    //当鼠标移动到目标li上时候slide_li宽和左边距等于当前元素，移开时候回到on_li对象上面
        Slide($(this));
    }, function () {
        Slide(on_li);
    });

});


$(function () {
    var item = $("tr");
    for (var i = 0; i < item.length; i++) {
        if (i % 2 == 0) {
            item[i].style.backgroundColor = "#f5f5f5";
        }
    }

    var select_all = $(".dateSelector").children();
    var manager_btn = $(".manager_btn");
    manager_btn.click(function () {
        var current_href = $(this).attr("href");
        var select_all = $(this).parent().parent().find("select");
        var current_y = select_all[0].value;
        var current_m = select_all[1].value;
        var current_d = select_all[2].value;
        window.open($(this).attr("href") + "&y=" + current_y + "&m=" + current_m + "&d=" + current_d);
        return false;

    });

    select_all.change(function () {
        //  select  td     tr
        var count_td = $(this).parent().parent().parent().children()[1];
        var current_y = $(this).parent().children()[0].value;
        var current_m = $(this).parent().children()[1].value;
        var current_d = $(this).parent().children()[2].value;
        var user_id = $(this).parent().attr("user_id");
        $.post("/post_count_select", {
            "date_y": current_y,
            "date_m": current_m,
            "date_d": current_d,
            "user_id": user_id
        }, function (data, status) {
            $(count_td).text(data);
        });
    });
//批量导入
    $("#import").click(function () {
        var html = '<div class="form-row"> <input type="file" name="filename" id="inputfile"/> </div>' +
            ' <div class="form-row"> </div>';
        new $.flavr({
            title: '上传文件', type: "file", content: '选择您的txt文件', dialog: 'form', form: {
                content: html, method: 'post', enctype: 'multipart/form-data', action: "/article_records_file"
            }, onSubmit: function ($container, $form) {
            }
        });  //return false;
    });

    $("#import").hover(
        function () {
            $(".tishi").fadeIn()
        }, function () {
            $(".tishi").fadeOut()
        });
    var poc = 0;

    function query(url, key, sum) {
        data = {"url": url, "key": key};
        post_url = "/tool/query_request2";
        $.post(post_url, data, function (result) {
            if (result != "null") {
                $("#th").after(result);
            }
            poc++;
            $("#progress_striped").css("width", Math.round(poc / sum * 100) + "%");
        });
        return 1
    }


    $("#query2-btn").click(function () {
        var url = $("#url").val();
        var key = $("#key").val();
        key_single = key.split("\n");
        $("#url_box").hide();
        $("#key_box").hide();
        $("#oTable").show(1500);
        for (i = 0; i < key_single.length; i++) {
            query(url, key_single[i]);
            $(this).hide("fast");
            $("#progress").show("slow");
            $("#query2-back-btn").fadeIn("slow");
            for (i = 0; i < key_single.length; i++) {
                if (query(url, key_single[i], key_single.length) == 1) {
                }
            }
        }
    });

    $("#query2-back-btn").click(function () {
        $("#progress").hide("fast");
        $("#url_box").show("slow");
        $("#key_box").show("slow");
        $("#oTable").hide();
        $("#oTable tr:gt(0)").remove();
        $(this).hide("fast");
        $("#query2-btn").fadeIn("slow");

    });

});

$(function () {
    //查询工具post
    function post_content() {
        var url = "/tool/query_request";
        var data = {"url": $("#url").val(), "key": $("#key").val()};
        CommonPerson.Base.LoadingPic.FullScreenShow();
        $.post(url, data, function (result) {
            if (result == "null") {
                CommonPerson.Base.LoadingPic.FullScreenHide();
            } else {
                CommonPerson.Base.LoadingPic.FullScreenHide();
                $("#result").val(result);//要刷新的div
            }
        });
    }

    $("#query-btn").click(function () {
        post_content();
    });
});