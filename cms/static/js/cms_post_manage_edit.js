/**
 * Created by rhj231223 on 2018/4/10.
 */

'use strict';


//编辑帖子函数
$(function(){
    var btn=$('#submit_btn');

    btn.click(function(event){
        event.preventDefault();

        var title = $('input[name=title]').val();
        var thumbnail = $('input[name=thumbnail]').val();
        var content = editor.txt.html();
        var tag_eles = $('label[data_check=1]');
        var tags=[];
        tag_eles.each(function(){
            tags.push($(this).attr('data_id'))
        });
        console.log(tags);

        rhjajax.post({
            url:window.location.href,
            data:{
                title:title,
                tags:tags,
                content:content,
            },
            success:function(data){
                if(data['code']===200){
                    xtalert.alertConfirm({
                        title:'发表成功!',
                        text:'帖子发表成功,是否再发一帖？',
                        confirmText:'继续发帖',
                        cancelText:'返回首页',
                        confirmCallback:function(){
                            setTimeout(function(){
                                window.location.reload()
                            },200)
                        },
                        cancelCallback:function(){
                            setTimeout(function(){
                                window.location='/cms/'
                            },200)
                        }
                    })
                }
            }
        })



    })
});

//编辑帖子的函数

$(function(){
    var btn=$('#edit_btn');

    btn.click(function(event){
        event.preventDefault();

        var article_id=$(this).attr('data_article_id');
        var title = $('input[name=title]').val();
        var thumbnail = $('input[name=thumbnail]').val();
        var content = editor.txt.html();
        var tag_eles = $('label[data_check=1]');
        var tags=[];
        tag_eles.each(function(){
            tags.push($(this).attr('data_id'))
        });
        console.log(tags);

        rhjajax.post({
            url:window.location.href,
            data:{
                article_id:article_id,
                title:title,
                tags:tags,
                content:content,
            },
            success:function(data){
                if(data['code']===200){
                    xtalert.alertSuccessToast(data['message']);
                    setTimeout(function(){
                        window.location='/cms/post_manage/'
                    },1000)
                }else{
                    xtalert.alertError(data['message'])
                }
            }
        })



    })
});