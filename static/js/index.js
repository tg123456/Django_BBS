$(function () {
    $("li.dropdown").click(function () {
        $(this).children("ul.dropdown-menu").css("display", "block")
    });
    $("li.dropdown").mouseenter(function () {
        $(this).children("ul.dropdown-menu").css("display", "block")
    });
    $("li.dropdown").mouseleave(function () {
        $(this).children("ul.dropdown-menu").css("display", "none")
    });
    $("ul.dropdown-menu").mouseleave(function () {
        $(this).css("display", "none")
    });

    $(".thumbs_Up").click(function () {
        var _this = this;
        var article_id = $(this).nextAll('input').attr("id");
        var user_id = $(this).nextAll('input').val();
        var is_up = 0

        if ($(this).hasClass("glyphicon-thumbs-down")){
            is_up = 0
        }
        if ($(this).hasClass("glyphicon-thumbs-up")){
            is_up = 1
        }

        $(".article").siblings().find(".thumbs_Up").next('span').text("");

        $.ajax({
            url: "/blog/thumbs_up/",
            type: "post",
            data: {
                is_up:is_up,
                user_id: user_id,
                article_id: article_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                console.log(data.up_down_num)
                if (data.code === 1) {
                    if(data.type === 'down'){
                        $(_this).text("反对("+data.up_down_num+")").css({"cursor":"pointer",'color':"#337ab7"})
                    }else{
                        $(_this).text("点赞("+data.up_down_num+")").css({"cursor":"pointer",'color':"#337ab7"})
                    }
                } else {
                    $(_this).next('span').text(data.error);
                }
            },
            error: function () {
                $(_this).next().text("登录后，才能给用户文章点赞和评论！");
                console.log("请求失败！");
            }
        });
    });




});
