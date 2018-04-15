/**
 * Created by rhj231223 on 2018/4/10.
 */

'use strict';

//标签函数
$(function () {
    var btn=$('.tag_btn');

    btn.click(function(event){
        event.preventDefault();
        var status=$(this).attr('data_check');
        console.log(status);

        if(status==='0'){
            $(this).attr('data_check','1');
            $(this).removeClass('btn-secondary');
            $(this).addClass('btn-success');
        }else{
            $(this).attr('data_check','0');
            $(this).removeClass('btn-success');
            $(this).addClass('btn-secondary');
        }

    });



});


//
$(function(){
    var btn=$('#add_tag');

    btn.click(function(event){
        event.preventDefault();

        xtalert.alertOneInput({
            title:'新增标签',
            text:'请输入新增标签的名称',
            placeholder:'例如 tornado',
            confirmCallback:function(inputValue){
                rhjajax.post({
                    url:'/cms/add_tag/',
                    data:{
                        name:inputValue,
                    },
                    success:function(data){
                        if(data['code']===200){
                            setTimeout(function(){
                                xtalert.alertSuccessToast(data['message'])
                            },100);
                            setTimeout(function(){
                                window.location.reload();
                            },1200)
                        }
                    }
                })
            },


        })

    })


});


//富文本编辑器

$(function(){
    var E=window.wangEditor;
    var editor=new E('#editor');
    editor.create();
    window.editor=editor
});

///七牛配置
$(function () {
    var upload_btn=$('#upload_btn');
    var form_progress=$('#form_progress');
    var progress_box=$('#progress_box');

    form_progress.css('display','none');

    xtqiniu.setUp({
        upload_btn:'upload_btn',

        success:function(up,file,info){
            var file_url=file.name;
            var tag='';

            if(file.type.indexOf('image')>=0){
               tag='<img src='+file_url+' alt="">';
            }else if(file.type.indexOf('video')>=0){
                tag='<video controls="controls" style="width: 640px;height:360px;">'+
                    '<source src='+file_url+'>'+
                '</video>'
            }
            window.editor.txt.append(tag);
        },
        fileadded:function(up,files){
            form_progress.show();
            upload_btn.attr('disabled','disabled');
            upload_btn.text('上传中...')
        },
        progress:function (up,file) {
            var percent=file.percent;
            progress_box.css('width',percent+'%');
            progress_box.attr('aria-valuenow',percent);
            progress_box.text(percent+'%');
        },
        complete:function(){
            progress_box.css({
                width:'2'+'%',
            });
            progress_box.attr('aria-valuenow','2');
            progress_box.text('0');
            progress_box.css('width','2%');
            upload_btn.prop('disabled',false);
            form_progress.hide();
            upload_btn.text('上传图片或视频');

        }

    })
});

//发布帖子函数
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
                }else{
                    xtalert.alertError(data['message'])
                }
            }
        })



    })
});
