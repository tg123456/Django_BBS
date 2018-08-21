$(function () {
    $("#login").click(function () {
        var username = $("#id_username").val();
        var password = $("#id_password").val();
        var csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val();
        var v_code = $("#v-code").val()
        // console.log(username)
        $.ajax({
            url:"/login/",
            type:'post',
            dataType:'json',
            data:{
                'username':username,
                'password':password,
                'v_code':v_code,
                'csrfmiddlewaretoken':csrfmiddlewaretoken
            },
            success:function (data) {
                // alert(data.code)
                if (data.code == 1){
                    window.location.href = '/index/'
                }else if (data.code == 2){
                    $("#error").text("验证码错误！")
                }else{
                    $("#error").text("用戶名或密碼錯誤！")
                }
            },
            error:function () {
                $("#error").text("請求失敗！")
            }
        });
    });

    // #有緩存,時間戳處理緩存問題
    $("#v-code-img").click(function (e) {
        var url_str = this.src
        var myDate = new Date().valueOf()
        var url = url_str.substr(0,29)
        this.src = url + myDate
    });


    var handlerPopup = function (captchaObj) {
        // 成功的回调
        captchaObj.onSuccess(function () {
            var validate = captchaObj.getValidate();
            $.ajax({
                url: "/login_slide_validate/", // 进行二次验证
                type: "post",
                dataType: "json",
                data: {
                    username: $("#id_username").val(),
                    password: $("#id_password").val(),
                    csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
                    geetest_challenge: validate.geetest_challenge,
                    geetest_validate: validate.geetest_validate,
                    geetest_seccode: validate.geetest_seccode
                },
                success: function (data) {
                    // captchaObj.hide();
                    if (data && (data.code === 1)) {
                        window.location.href = '/index/';
                        // $(document.body).html('<h1>登录成功</h1>');
                    } else {
                        $("#error").text("用戶名或密碼錯誤！");
                        // $(document.body).html('<h1>登录失败</h1>');
                    }
                }
            });
        });
        $("#login_sv").click(function () {
            captchaObj.show();
        });
        // 将验证码加到id为captcha的元素里
        captchaObj.appendTo("#popup-captcha");
        // 更多接口参考：http://www.geetest.com/install/sections/idx-client-sdk.html
    };
    // 验证开始需要向网站主后台获取id，challenge，success（是否启用failback）
    $.ajax({
        url: "/pcgetcaptcha/?t=" + (new Date()).getTime(), // 加随机数防止缓存
        type: "get",
        dataType: "json",
        success: function (data) {
            // 使用initGeetest接口
            // 参数1：配置参数
            // 参数2：回调，回调的第一个参数验证码对象，之后可以使用它做appendTo之类的事件
            initGeetest({
                gt: data.gt,
                challenge: data.challenge,
                product: "popup", // 产品形式，包括：float，embed，popup。注意只对PC版验证码有效
                offline: !data.success // 表示用户后台检测极验服务器是否宕机，一般不需要关注
                // 更多配置参数请参见：http://www.geetest.com/install/sections/idx-client-sdk.html#config
            }, handlerPopup);
        }
    });

    
});