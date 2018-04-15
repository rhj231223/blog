/**
 * Created by rhj231223 on 2018/4/15.
 */

'use strict';


    // 评论功能函数
$(function(){
    var btn=$('#comment_btn');
    btn.click(function(event){
        event.preventDefault();

        var user=$('#svg_div').attr('data_username');
        var username='';
        var article_id=$('#add_comment_form').attr('data_article_id');

        var content=$('input[name=content]').val();

        if(user){
            console.log(1);
            username=user
        }else{
            console.log(2);
            username=$('input[name=username]').val();
        }


        rhjajax.post({
            url:'/add_comment/',
            data:{
                article_id:article_id,
                username:username,
                content:content,
            },
            success:function (data) {
                if(data['code']===200){
                    xtalert.alertSuccessToast(data['message']);
                    setTimeout(function(){
                        window.location.reload();

                    },1200);
                }else{
                    xtalert.alertError(data['message'])
                }
            }
        })



    })

});

