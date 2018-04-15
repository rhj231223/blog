/**
 * Created by renhuijun on 2017/8/4.
 */
'use strict';
$(function(){
    var graph_btn=$('#graph_btn');
    graph_btn.click(function(event){
        event.preventDefault();

        var old_src='/common/captcha/';
        var new_src=xtparam.setParam(old_src,'xxx',Math.random())
        $(this).attr('src',new_src);
    })
});