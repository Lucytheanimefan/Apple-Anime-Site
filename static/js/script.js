var height = $(window).height();
var imacRatio = 0.68; //screen height by full height of imac
var imacScreenRatio = 1.71; //width by height


$(document).ready(function() {
    imacHeight = height * 0.85;
    iframeHeight = imacHeight * imacRatio;
    iframeWidth = iframeHeight * imacScreenRatio;
    imacScreenHeight = imacHeight * 0.75;
    $("#imac").css("height", imacHeight + "px");
    var imacWidth = $("#imac").width();
    $("body").css("min-width", imacWidth);
    var iframePadding = (imacWidth - iframeWidth) / 2;
    var iframePaddingTop = (imacScreenHeight - iframeHeight) / 2;

    console.log(iframeWidth)
    console.log(iframeHeight)

    $("#youtube").css({ "width": iframeWidth+"px","padding-left": iframePadding, "padding-right": iframePadding, "padding-top": iframePaddingTop });
    $("section").css("min-height", imacHeight + "px");




})


/* --- youtube ----*/
var player, playing = false;

function onYouTubeIframeAPIReady() {
    player = new YT.Player('youtube', {
        height: iframeHeight,
        width: iframeWidth,
        videoId: 'fzQ6gRAEoy0',
        events: {
            'onStateChange': onPlayerStateChange
        }
    });
}

function onPlayerStateChange(event) {
    if (!playing) {
        alert('hi');
        playing = true;
    }
}
