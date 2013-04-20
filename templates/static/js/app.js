$(function(){
    setHeight()
    $(window).resize(function(){setHeight()})

    $('.scroll-pane').jScrollPane({
        autoReinitialise:true
    });
})

function setHeight() {
    var sidebarHeight = 65;
    var height = $(window).height() - sidebarHeight;
    $(".scroll-pane").height(height);
}