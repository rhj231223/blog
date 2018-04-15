/**
 * Created by rhj231223 on 2018/4/8.
 */

'use strict';

$(function () {
    $('.captcha_img').click(function(){
        const href=window.location.href;
        window.location=xtparam.setParam(href,'show',Math.random())

    });
});
