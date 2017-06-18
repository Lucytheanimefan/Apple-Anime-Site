var height = $(window).height();
var imacRatio = 0.68; //screen height by full height of imac
var imacScreenRatio = 1.71; //width by height


$(document).ready(function() {
    if (localStorage.getItem("visitedAnime@Apple") == null) {
        localStorage.setItem("visitedAnime@Apple", true);
    } else {
    	mainPage();
    }
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

    $("#youtube").css({ "width": iframeWidth + "px", "padding-left": iframePadding, "padding-right": iframePadding, "padding-top": iframePaddingTop });
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

var shrinkSpeed = 300;

function mainPage() {
    $(".phone").remove();
    $("#mainVideo").css("margin-top", "60px");
    $(".navbar").css({
        "display": "inline",
        "z-index": "5"
    });
}

function onPlayerStateChange(event) {
    console.log(event);
    if (!playing) {
        if (localStorage.getItem("visitedAnime@Apple") == null) {
            mainPage();
        }
        /*$("#grid").css("display", "inline");
        
        setTimeout(function() {
            $("#grid").animate({
                left: "-=" + (shrinkSpeed*2),
                top: "-=" + (shrinkSpeed - 240),
                width: "-=" + shrinkSpeed*1.5,
                height: "-=" + shrinkSpeed*1.5
            }, 5000, function() {
                // Animation complete.
            });
        }, 2000);
*/

        playing = true;
    }
}
