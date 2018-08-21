$(function () {
    // $("#register1").click(function () {
    //     var username = $("#id_username").val()
    //     var password = $("#id_password").val()
    //     var rep_password = $("#id_rep_password").val()
    //     var phone = $("#id_phone").val()
    //     var email = $("#id_email").val()
    //     var v_code = $("#v_code").val()
    //     var csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val();
    //     console.log("v_code = ",v_code);
    //     $.ajax({
    //         url:'/register/',
    //         type:'post',
    //         data:{
    //             "username":username,
    //             "password":password,
    //             "rep_password":rep_password,
    //             "phone":phone,
    //             "email":email,
    //             "v_code":v_code,
    //             "csrfmiddlewaretoken":csrfmiddlewaretoken,
    //         },
    //         success:function (data) {
    //             if (data.code == 1){
    //                 window.location.href = '/login/'
    //             }else if (data.code == 2){
    //                 $("#error").text("验证码错误！")
    //             }else{
    //                 $.each(data.error,function (k,v) {
    //                     // console.log($("id_"+k).parent().next()[0])
    //                     // $("id_"+k).parent().next().text(v)
    //                     // $("#"+k).text(v)
    //                 });
    //             }
    //         },
    //         error:function () {
    //             console.log("请求失败！")
    //         }
    //     });
    // });

    $("#register").click(function () {
        var username = $("#id_username").val();
        var password = $("#id_password").val();
        var rep_password = $("#id_rep_password").val();
        var phone = $("#id_phone").val();
        var email = $("#id_email").val();
        var v_code = $("#v_code").val();
        var csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val();

        var flag = 0;
        if(username === "" | username == null){
            flag = 1;
            $("#username").text("姓名不能为空！");
            $("#id_username").focus(function () {
                $("#username").text("");
            });
        }
        if(password === "" | password == null){
            flag = 1;
            $("#password").text("密码不能为空！");
            $("#id_password").focus(function () {
                $("#password").text("");
            });
        }
        if(rep_password === "" | rep_password == null){
            flag = 1;
            $("#rep_password").text("确认密码不能为空！");
            $("#id_rep_password").focus(function () {
                console.log("id_rep_password");
                $("#rep_password").text("");
            });
        }
        if(phone === "" | phone == null){
            flag = 1;
            $("#phone").text("电话号码不能为空！");
            $("#id_phone").focus(function () {
                $("#phone").text("");
            });
        }
        if(email === "" | email == null){
            flag = 1;
            $("#email").text("邮箱不能为空！");
            $("#id_email").focus(function () {
                $("#email").text("");
            });
        }
        if(v_code === "" | v_code == null){
            flag = 1;
            $("#error").text("验证码不能为空！");
            $("#v_code").focus(function () {
                $("#error").text("");
            });
        }

        if(flag === 1){ return false; }


        var fd = new FormData();
        fd.append("username",username);
        fd.append("password",password);
        fd.append("rep_password",rep_password);
        fd.append("phone",phone);
        fd.append("email",email);
        fd.append("csrfmiddlewaretoken",csrfmiddlewaretoken);
        fd.append('avatar', $("#avatar")[0].files[0]);
        fd.append('v_code',$("#v_code").val());

        $.ajax({
            url:'/register/',
            type:'post',
            processData:false,
            contentType:false,
            data:fd,
            success:function (data) {
                if (data.code == 1){
                    window.location.href = '/login_slide_validate/'
                }else if (data.code == 2){
                    $("#error").text("验证码错误！")
                    $("#error").focus(function () {
                            $("#error").text("");
                        });
                }else{
                    $.each(data.error,function (k,v) {
                        $("#"+k).text(v);
                        $("#id_"+k).focus(function () {
                            $("#"+k).text("");
                        });
                    });
                }
            },
            error:function () {
                console.log("请求失败！")
            }
        });
    });

    $("#v-code").focus(function () {
        $("#error").text("")
    });

     // #有緩存,時間戳處理緩存問題
    $("#v_code_img").click(function (e) {
        var url_str = this.src
        var myDate = new Date().valueOf()
        var url = url_str.substr(0,29)
        this.src = url + myDate
    });

    //头像预览
    //当input框选中文件之后，也就是文件input有值之后触发
    $("#avatar").change(function () {
        var file = this.files[0];
        //生成一个读文件方法
        var fr = new FileReader();
        //从文件中读取数据
        fr.readAsDataURL(file);
        //等到读完之后
        fr.onload = function () {
            //头像img标签的src换一下
            $("#avatar-img").attr("src",fr.result)
        }
    });

    // 每一个input标签获取焦点的时候，把自己下面的span标签内容清空，把父标签的has-error样式移除

});







