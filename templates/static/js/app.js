$(function(){
    setHeight()
    $(window).resize(function(){setHeight()})
})

function setHeight() {
    var sidebarHeight = 65;
    var height = $(window).height() - sidebarHeight;
    $("#sidebar-1").height(height);
    $("#sidebar-2").height(height);
    $("#main-content-area").height(height); 
}