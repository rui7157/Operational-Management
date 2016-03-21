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

$(function(){
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
        $("#ad_setting_ul").show();
    });
    $("#ad_setting_ul").mouseleave(function () {
        $(this).hide();
    });
    $("#ad_setting_ul li").mouseenter(function () {
        $(this).find("a").attr("class", "ad_setting_ul_li_a");
    });
    $("#ad_setting_ul li").mouseleave(function () {
        $(this).find("a").attr("class", "");
    });


    //检验输入框
    $("#check_pwd2").blur(function(){
        if ($("#check_pwd1").val() != $(this).val()){
             new $.flavr('两次输入密码不一致！');
            $("#ok_btn").attr("class","btn disabled");
        }else{
            if ($("#check_pwd1").val() == ""){
                new $.flavr('输入密码不能为空！');
                $("#ok_btn").attr("class","btn disabled");
            }else{
                $("#ok_btn").attr("class","btn");
            }
        }
    });
});