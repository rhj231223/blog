/**
 * Created by rhj231223 on 2018/4/9.
 */

'use strict';

// 发送邮件的函数
$(function () {
    var send_btn=$('#send_btn');

    send_btn.click(function(event){
        event.preventDefault();

        var email=$('input[name=email]').val();

        rhjajax.post({
            url:'/cms/send_mail/',
            data:{
                email:email
            },
            success:function(data){
                if(data['code']===200){
                    xtalert.alertSuccessToast(data['message']);

                    var count=120;

                    send_btn.attr('disabled','disabled');

                    var timer=setInterval(function(){
                        send_btn.text(count);

                        if(count<=0){
                            clearInterval(timer);
                            send_btn.prop('disabled',false);
                            send_btn.text('发送邮件');
                        }

                        count-=1

                    },1000)


                }else{
                    xtalert.alertError(data['message'])
                }


            }
        })


    })

});

//修改邮箱的函数

$(function(){
    var submit_btn=$('#submit_btn');
    submit_btn.click(function(event){
        event.preventDefault();

        var email=$('input[name=email]');
        var email_captcha=$('input[name=email_captcha]');

        rhjajax.post({
            url:window.location.href,
            data:{
                email:email.val(),
                email_captcha:email_captcha.val(),
            },
            success:function(data){
                if(data['code']===200){
                    xtalert.alertSuccessToast(data['message']);
                    email.val('');
                    email_captcha.val('');
                }else{
                    xtalert.alertError(data['message'])
                }
            }

        })

    })

});