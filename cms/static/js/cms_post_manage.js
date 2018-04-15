/**
 * Created by rhj231223 on 2018/4/11.
 */

'use strict';

$(function () {
    var btn = $('.delete_btn');
    btn.click(function(event){
        event.preventDefault();


        var article_id=$(this).attr('data_article_id');
        var to_delete=$(this).attr('data_article_id');

        var to_delete=parseInt(to_delete);

        rhjajax.post({
            url:'/cms/post_manage_delete/'+article_id+'/',
            data:{
                article_id:article_id,
                to_delete:to_delete,
            },
            success:function(data){
                if(data['code']===200){
                    xtalert.alertSuccessToast(data['message']);
                    setTimeout(function(){
                        window.location.reload();
                    },1200)
                }else{
                    xtalert.alertError(data['message'])
                }
            },
        })

    });

});

//页面跳转的函数
$(function(){
    var btn=$('#btn_page');
    btn.click(function(event){
        event.preventDefault();

        var page=$('input[name=input_page]').val();
        window.location='/cms/post_manage/'+page+'/';
        var li=window.location.search.split('?');
        if(!li[1]){
            window.location='/cms/post_manage/'+page+'/'
        }else{
            window.location='/cms/post_manage/'+page+'/'+'?'+li[1];
        }

    })
});