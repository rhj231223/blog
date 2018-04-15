/**
 * Created by rhj231223 on 2018/4/9.
 */

'use strict';

$(function () {
    var href=window.location.href;



    if(href.indexOf('profile')> 0){
        $('#profile').addClass('now_page')
    }else if(href.indexOf('user_manage')> 0){
        $('#user_manage').addClass('now_page')
    }else if(href.indexOf('post_manage')> 0){
        $('#post_manage').addClass('now_page')
    }else if(href.indexOf('comment_manage')> 0){
        $('#comment_manage').addClass('now_page')
    }else{
         $('#index').addClass('now_page')
    }

    console.log(href)
});


//搜索函数
//
// $(function(){
//     var search_input=$('input[name=search]');
//     search_input.bind('keypress',function(event){
//         if(event.keyCode==='13'){
//             var search_content=search_content.val();
//             window.location='/cms/search/'+search_content+'/1/';
//         }
//     })
// });
