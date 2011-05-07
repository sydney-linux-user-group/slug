/*
 * -*- coding: utf-8 -*-
 * vim: set ts=2 sw=2 et sts=2 ai:
 *
 * YoutubeCloud - jQuery plugin
 *
 * Based on the idea at http://alvaromontoro.com/youtubeCloud/ but using the
 * new HTML5 compatible API.
 */

var yt_zindex = 0;

(function ($) {

	$.fn.youtubecloud=function (playerVars) {

    var defaultVars = {
      loop: 1, 
      controls: 0
    };
    if (!playerVars) {
      playerVars = defaultVars;
    }

    // We need this parameter otherwise it won't work.
		playerVars.allowScriptAccess = "always";
    playerVars.enablejsapi = 1;

    var parent_width = $(this).width();
    var parent_height = $(this).height();

    $(this).find("div").each(function(index, div) {
      var playerID = "ytc_player" + index;
      
      var div = $(div);
      div.attr("id", playerID);
      // Save the div properties for later
      var orig_width = div.width();
      var orig_height = div.height();

      // Put the divs in random locations inside their parent.
      var new_top = Math.round(Math.random()*(parent_height-orig_height));
      var new_left = Math.round(Math.random()*(parent_width-orig_width));
      div.css('position', 'absolute');
      div.css('top', new_top+'px');
      div.css('left', new_left+'px');

      div.css('display', 'none');
      var player = new YT.Player(playerID, {
        width: "100%",
        height: "100%",
        videoId: div.attr("data"),
        playerVars: playerVars,
        events: {
          'onReady': function(event) {
            div.css('display', '');
            // Mute doesn't work on HTML5 videos
            event.target.setVolume(0); 
            event.target.playVideo();
          },
        }
	    }); // YT.Player

      window.setTimeout(function() {
        if (div.css('display') == "none") {
          console.log('YouTube ' + playerID + ' was unable to load ' + div.attr('data') + ' ' + div.css('display'));
        } else {
          console.log('YouTube ' + playerID + ' loaded ' + div.attr('data') + ' fine!');
        }
      }, 15000);

      function volume (now, fx) {
        if (fx.prop == 'width') {
          player.setVolume((now-orig_width)/parent_width*100);
        }
      }

      // Make it bigger!
      div.mouseenter(function() {
        // Clear any animation
        div.stop();

        // Make us ontop
        yt_zindex++;
        div.css('z-index', yt_zindex);

        // We need to calculate the duration as we might be half way through an
        // animation.
        var duration = (parent_width - div.width())/parent_width * 4000;

        // Animate!
        div.animate({
          top: 0,
          left: 0,
          width: parent_width,
          height: parent_height,
        }, {
          duration: duration,
          step: volume
        })
      }); // div.onmouseenter

      // Make it smaller
      div.mouseleave(function() {
        // Clear any animation
        div.stop();

        // We need to calculate the duration as we might be half way through an
        // animation.
        var duration = (1-(parent_width - div.width())/parent_width) * 4000;

        // Animate!
        div.animate({
          top: new_top,
          left: new_left,
          width: orig_width,
          height: orig_height,
        }, {
          duration: duration,
          step: volume
        });
      }); // div.onmouseleave
    }); // each
  }; // youtubecloud
})(jQuery);
