var height = $(window).height();
var imacRatio = 0.68; //screen height by full height of imac
var imacScreenRatio = 1.71; //width by height


$(document).ready(function() {
    var imacHeight = height * 0.85;
    var iframeHeight = imacHeight * imacRatio;
    var iframeWidth = iframeHeight * imacScreenRatio;
    var imacScreenHeight = imacHeight * 0.75;
    $("#imac").css("height", imacHeight + "px");
    var imacWidth = $("#imac").width();
     $("body").css("min-width",imacWidth);
    var iframePadding = (imacWidth - iframeWidth) / 2;
    var iframePaddingTop = (imacScreenHeight - iframeHeight)/2;
    $("#youtube").css({ "width": iframeWidth, "height": iframeHeight, "padding-left": iframePadding, "padding-right": iframePadding, "padding-top":iframePaddingTop });
    $("section").css("min-height",imacHeight+"px");




})
