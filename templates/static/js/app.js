$(function(){
    setHeight();
    $(window).resize(function(){setHeight();});

    $('.scroll-pane').jScrollPane({
        autoReinitialise:true
    });

    // $(".sub-ul").hide();
    $(".side-nav li span").click(function(){
        $(this).parent('li').find('ul.sub-ul').slideToggle();
    });

    if($('ul.settings a.edit-link').length) {
        $('ul.settings form').hide();
        $('ul.settings a.edit-link').click(function(event){
            event.preventDefault();
            $(this).next().next('form').toggle();
        });
    }
});

function setHeight() {
    var sidebarHeight = 115;
    var height = getWindowSize().height - sidebarHeight;
    // alert(height)
    $(".scroll-pane").height(height);
}

function getWindowSize() {
    var myWidth = 0, myHeight = 0;
    if( typeof( window.innerWidth ) == 'number' ) {
        //Non-IE
        myWidth = window.innerWidth;
        myHeight = window.innerHeight;
    } else if( document.documentElement && ( document.documentElement.clientWidth || document.documentElement.clientHeight ) ) {
        //IE 6+ in 'standards compliant mode'
        myWidth = document.documentElement.clientWidth;
        myHeight = document.documentElement.clientHeight;
    } else if( document.body && ( document.body.clientWidth || document.body.clientHeight ) ) {
        //IE 4 compatible
        myWidth = document.body.clientWidth;
        myHeight = document.body.clientHeight;
    }
    result = {
        'width' : myWidth,
        'height': myHeight
    };

    return result;
}