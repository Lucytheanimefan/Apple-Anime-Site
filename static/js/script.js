var height = $(window).height();
var imacRatio = 0.7036; //screen height by full height of imac
var imacScreenRatio = 1.63; //width by height


$(document).ready(function() {
    var imacHeight = height * 0.9;
    var iframeHeight = imacHeight * imacRatio;
    var iframeWidth = iframeHeight * imacScreenRatio;
    console.log($("#imac").width() +"-" + iframeWidth);
    console.log(iframePadding)
    $("#imac").css("height", imacHeight + "px");
    var iframePadding = ($("#imac").width() - iframeWidth) / 2;
    $("#youtube").css({ "width": iframeWidth, "height": iframeHeight, "padding-left": iframePadding, "padding-right": iframePadding });

    


})
