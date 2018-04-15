/**
 * Created by rhj231223 on 2018/4/13.
 */

'use strict';
//翻页功能函数
$(function () {
    var btn=$('#btn_page');
    btn.click(function(event){
        event.preventDefault();

        var page=$('input[name=input_page]').val();

        window.location=/articles/+page+'/';


    })
});


//搜索功能的函数

$(function(){
    var btn=$('input[name=search]');
    btn.bind('keypress',function(event){
        if(event.keyCode==='13'){
            window.location='/articles/1/?search='+btn.val()
            alert(1);
        }
    })
});
