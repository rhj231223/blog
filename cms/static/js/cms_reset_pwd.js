/**
 * Created by rhj231223 on 2018/4/9.
 */

'use strict';

$(function () {
    var btn=$('#reset_pwd_btn');
    btn.click(function(event){
        event.preventDefault();

        const old_pwd=$('input[name=old_pwd]');
        const new_pwd=$('input[name=new_pwd]');
        const new_pwd_repeat=$('input[name=new_pwd_repeat]');

        rhjajax.post({
            url:window.location.href,
            data:{
                old_pwd:old_pwd.val(),
                new_pwd:new_pwd.val(),
                new_pwd_repeat:new_pwd_repeat.val(),
            },
            success:function (data) {
                if(data['code']===200){
                    xtalert.alertSuccessToast(data['message'])
                    old_pwd.val('');
                    new_pwd.val('');
                    new_pwd_repeat.val('');

                }else{
                    xtalert.alertError(data['message'])
                }
            }
        })

    })

});
