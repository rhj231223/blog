/**
 * Created by rhj231223 on 2018/4/10.
 */

'use strict';

$(function () {
    var black_btn=$('.black_btn');

    black_btn.click(function(event){
        event.preventDefault();

        var user_id=$(this).attr('data_user_id');
        var to_active=$(this).attr('data_to_active');

        rhjajax.post({
            url:'/cms/black/',
            data:{
                user_id:user_id,
                to_active:to_active,
            },
            success:function(data){
                if(data['code']===200){
                    var msg='';
                    if(to_active==='0'){
                        msg='已拉黑!'
                    }else{
                        msg='已解禁'
                    }
                    xtalert.alertSuccessToast(msg);
                    setTimeout(function(){
                    window.location.reload();
                },1200)
                }else{
                    xtalert.alertError(data['message']);
                }


            }
        })

    });
});
