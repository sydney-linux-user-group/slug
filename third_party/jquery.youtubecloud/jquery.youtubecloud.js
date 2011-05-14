/*
 * -*- coding: utf-8 -*-
 * vim: set ts=2 sw=2 et sts=2 ai:
 *
 * YoutubeCloud - jQuery plugin
 *
 * Based on the idea at http://alvaromontoro.com/youtubeCloud/ but using the
 * new HTML5 compatible API.
 */

var ytcloud_zindex = 0;

function inside(value, min, max) {
  return (value <= max) && (value >= min);
}
function collide(a, b) {
  var padding = 5;
  var left_overlap = 
    inside(a.left, b.left, b.left + b.width + padding) || 
    inside(b.left, a.left, a.left + a.width + padding);
  var top_overlap = 
    inside(a.top, b.top, b.top + b.height + padding) || 
    inside(b.top, a.top, a.top + a.height + padding);
  return left_overlap && top_overlap;
}

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

    var already_positioned = [];
    var divs = $(this).find("div");
    divs.each(function(index, div) {
      var playerID = "ytc_player" + index;
      
      var div = $(div);
      div.attr("id", playerID);
      div.attr("class", "box");
      // Save the div properties for later
      var orig_width = div.width();
      var orig_height = div.height();

      // Put the divs in random locations inside their parent.
      var attempts = 0;
			while (attempts < 1000) {
        var new_height = Math.round(Math.random()*(parent_width*0.20)+(parent_width*0.05));
        var new_width = Math.round(new_height*(4.0/3));
        var new_top = Math.round(Math.random()*(parent_height-new_height));
        var new_left = Math.round(Math.random()*(parent_width-new_width));

        var collisions = false;
        $.each(already_positioned, function(index, other_div) {
          collisions = collisions || collide(
            {top: new_top, left: new_left, width: new_width, height: new_height},
            other_div);
        });

        if (collisions) {
          attempts++;
          continue;
        }

        already_positioned.push({
          height: new_height,
          width: new_width,
          top: new_top,
          left: new_left
        });
        break;
      }
      console.log('Found a position after', attempts, 'iterations');
      div.css('position', 'absolute');
      div.css('top', new_top+'px');
      div.css('left', new_left+'px');
      div.css('width', new_width+'px');
      div.css('height', new_height+'px');

      div.css('display', 'none');
      var player = new YT.Player(playerID, {
        width: "100%",
        height: "100%",
        videoId: div.attr("data"),
        playerVars: playerVars,
        events: {
          'onReady': function(event) {
            div.fadeIn();
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
        ytcloud_zindex++;
        div.css('z-index', ytcloud_zindex);

        // We need to calculate the duration as we might be half way through an
        // animation.
        var duration = (parent_width - div.width())/parent_width * 4000;

        // Animate!
        div.animate({
          top: 0,
          left: 0,
          width: '+='+(parent_width-div.width()),
          height: '+='+(parent_height-div.height()),
        }, {
          duration: duration,
          step: volume
        });
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
          width: new_width,
          height: new_height,
        }, {
          duration: duration,
          step: volume
        });
      }); // div.onmouseleave
    }); // each
  }; // youtubecloud
})(jQuery);
