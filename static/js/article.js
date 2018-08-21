$(function () {

    $(".list-group").on('click','.replay',function () {
        var $commentsContent = $("#commentsContent");
        var parent_comment_id = $(this).attr("comment_id");
        var parent_comment_name = $(this).prev('span').text();
        console.log("parent_comment_name = ",parent_comment_name);
        $commentsContent.data("parent_comment_id",parent_comment_id);
        $commentsContent.data("parent_comment_name",parent_comment_name);
        var str = "(@ "+ parent_comment_name +" )";

        $("#errorMessage").val("@"+parent_comment_name);
        $("#errorMessage").css("color",'red');

        $commentsContent.focus().val("@"+parent_comment_name+"\n");
    })

    $("#commentsContent").focus(function () {
        $(this).css({'border':"1px solid rgb(169, 169, 169)"});
        $("#errorMessage").css('color','black').val("");
    });

    // #上传评论
    $("#submitComment").click(function () {
        var _this = this;
        var $commentsContent = $("#commentsContent");
        var content = $commentsContent.val();
        var hiddenInfo = $("#hiddenInfo").val().split('|');

        var parent_comment_id =$commentsContent.data("parent_comment_id")||"";
        var parent_comment_name =$commentsContent.data("parent_comment_name")||"";

        console.log(parent_comment_id);
        console.log("submitComments");
        console.log("content");

        if (parent_comment_id){
            content = content.slice(content.indexOf('\n')+1,);
        }

        if(content === "" | content == null){
            $("#errorMessage").css("color","red").val("评论内容不能为空！"),
            //清空之前保存的信息
            // $commentsContent.data("parent_comment_id",'');
            // $commentsContent.data("parent_comment_name",'');

            $commentsContent.css({
                'border':"1px solid red",
            });
            return;
        };

        content =  "@"+parent_comment_name+":  "+content;

        $.ajax({
            url:'/blog/comment/',
            type:"post",
            data:{
                "user_id":hiddenInfo[0],
                "article_id":hiddenInfo[1],
                "reviewer_id":hiddenInfo[2],
                "parent_comment_id":parent_comment_id,
                "content":content,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success:function (data) {
                console.log(data);
                //添加dom对象，使用模板语言
                var comment_amount = $(".list-group").children("div").length;
                console.log("comment_amount = ",comment_amount);
                if(data.code === 1){
                    //清空之前保存的信息
                    $commentsContent.data("parent_comment_id",'');
                    $commentsContent.data("parent_comment_name",'');

                    $("#comment_count").text("评论("+data.comment_count+") ");
                    $commentsContent.val("");
                    var contentHtml =
                    `<div type="button" class="list-group-item">
                        <h4 style="border-bottom: dashed 1px #c0c0c0">
                            <span>#${ comment_amount+1 }楼</span>
                            ${data.build_owner}
                            <span>${ data.create_time }</span>
                            <span>|</span>
                            <span>${ data.username }</span>
                            <span comment_id="${ data.comment_id }"  class="pull-right replay" style="cursor: pointer">回复</span>
                        </h4>
                        <!-- 评论的内容 -->
                        <p class="list-group-item-text">${ data.content }</p>
                        <!-- 评论的内容 -->
                    </div>`;
                $(".list-group").append(contentHtml);
                }else {
                    $("#errorMessage").css("color","red").val(data.error);
                    $("#commentsContent").val(content);
                }
            },
            error:function () {
                $("#errorMessage").css("color","red").val("发送请求失败！");
                console.log("发送请求失败！")
            }
        });
    });

    $("#unpublish").click(function () {
        window.location.href = '/blog/backend';
    });

    $("#cancel").click(function () {
        $("#myModal").modal("hide");
        return false;
    });

    $("#sure").click(function () {
        $("#myModal").modal("hide");
        var article_id = $("#sure").attr("name");
        console.log("article_id = ",article_id);
        console.log(id);
        $.ajax({
            type: "post",
            url: "/blog/del_article/",
            dataType: "json",
            data: {
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
                "article_id": article_id,
            },
            success: function (data) {
                if(data.code == 1){
                    window.location.href = "/blog/backend/"
                }else {
                    $("#message").css("color","red").val(data.message);
                }
            },
            error: function () {
                $("#message").css("color","red").val("操作失败！")
            }
        });
    });

});

