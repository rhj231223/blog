/**
 * Created by rhj231223 on 2018/4/12.
 */

'use strict';

$(function () {
    var btn=$('.icon_search_click');
    var search=$('.search_component');
    var cancel_btn=$('.cancel_search_btn');
    btn.click(function(event){
        // event.preventDefault();

        btn.hide();
        search.slideToggle(200);


    });

    cancel_btn.click(function(event){
            event.preventDefault();
            search.hide();
            btn.slideDown();
        })


});
