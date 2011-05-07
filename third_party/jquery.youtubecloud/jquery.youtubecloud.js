/*
 * YoutubeCloud - jQuery plugin 2.0
 *
 * Copyleft (c) 2011 Alvaro Montoro Dominguez
 *
 * Licensed under the GPL license:
 *   http://www.gnu.org/licenses/gpl.html
 *
 */		
 
// global variables, my programming professor would kill me if he sees this code
var arrayVideoIds = [];
var numVideos = 0;

// this is a Youtube API function. If you are using this API already, you may want to redefine
function onYouTubePlayerReady(playerId) {
	// get the player
	var ytplayer = document.getElementById(playerId);
	
	// add some additional information
	if (!ytplayer.information) { ytplayer.information = { 'videoID':arrayVideoIds[playerId] } }
	
	// load the video, set the quality and mute it
	ytplayer.loadVideoById(ytplayer.information.videoID);
	ytplayer.mute();
	ytplayer.setPlaybackQuality(settings.quality);
	
	// add the event listener for that particular video
	ytplayer.addEventListener("onStateChange", "onytplayerStateChange");
}

// this is another Youtube API function. Video event listenet onStateChange, you may want to redefine if you are using the API already.
function onytplayerStateChange(newState) {
	var aux = 0;
	// we don't know who is the caller, so we iterate through all the videos updating state if necessary
	while (document.getElementById('ytc_player'+aux)) {
		var player = document.getElementById('ytc_player'+aux);
		// if the video has finished, we restart it
		if (player.getPlayerState() == 0) { player.seekTo(0, true); }
		aux++;
	}
}

// this function mutes ALL the videos on the page (that are from a youtubecloud div
function ytc_mute_all_videos() {
	var aux = 0;
	while (document.getElementById('ytc_player'+aux)) {
		var player = document.getElementById('ytc_player'+aux);
		player.mute();
		aux++;
	}
}
		
;(function ($) {

	$.fn.youtubecloud=function (options) {

		settings = {
			'width':600,
			'height':400,
			'videoWidth': 100,
			'proportion': 0.75,
			'grow':2,
			'flashVersion': 8,
			'quality':'small',
			'speed': 1000,
			'pause': false,
			'borderSize': 5,
			'borderStyle': 'solid',
			'borderColor': '#800000'
		};
		    
		return this.each(function () {
		
			// extend the default settings
			if ( options ) { $.extend( settings, options ); };
            
			arrayVideos = [];
			arrayVideoIds = [];
			numVideos = 0;
			ytc_exit = 0;

			$(this).find("span").each(function() {
		
				function ytc_calculate_collisions(posX, posY, arrVids, sett) {
					
					if (posX/1+sett.videoWidth/1 > sett.width) { return 1; }
					if (posY/1+sett.videoWidth*sett.proportion > sett.height) { return 1; }
					
					var x = 0;
					
					for (x=0; x<arrVids.length;x++) {
						
						var a1=arrVids[x][0];
	                    var a2=arrVids[x][1];
	                    var b1=posX;
	                    var b2=posY;
	                    var awidth=arrVids[x][2];
	                    var aheight=arrVids[x][3];
	                    var bwidth=sett.videoWidth;
	                    var bheight=sett.videoWidth*sett.proportion;
	                    
	                    if (eval("b1>=a1 && b1<=a1+awidth+15 && b2>=a2 && b2<=a2+aheight+15")) { return 1; }
	                    if (eval("a1>=b1 && a1<=b1+bwidth+15 && a2>=b2 && a2<=b2+bheight+15")) { return 1; }
	                    if (eval("b1>=a1 && b1<=a1+awidth+15 && a2>=b2 && a2<=b2+bheight+15")) { return 1; }
	                    if (eval("a1>=b1 && a1<=b1+bwidth+15 && b2>=a2 && b2<=a2+aheight+15")) { return 1; }
						
					}
					
					return 0;
					
				}
				
				var divID = "ytc_frame" + numVideos
				var videoID  = $(this).text().replace("http://www.youtube.com/watch?v=","");
				var playerID = "ytc_player" + numVideos;
				var params = { allowScriptAccess: "always" };
				var atts = { id: playerID };
				var divVideo = $(this);

				arrayVideoIds[playerID] = videoID;
				
				$(this).attr("id", divID);
				$(this).css({border:"5px solid #800000",backgroundColor:settings.borderColor,width:100,height:75 });
				
				// CALCULATE POSITIONS!!!
				if (numVideos == 0) {
					ytc_posX = 0;
					ytc_posY = 0;
					var videoType = [ytc_posX, ytc_posY, settings.videoWidth, settings.videoWidth*settings.proportion];
					arrayVideos.push(videoType);
				} else {
					
					ytc_exit = 0;
					ytc_attempts = 0;
					
					while (ytc_exit == 0 && ytc_attempts < 1000) {
						ytc_posX = Math.floor(Math.random() * (settings.width-settings.videoWidth));
						ytc_posY = Math.floor(Math.random() * (settings.height-settings.videoWidth*settings.proportion));
						
						if (ytc_calculate_collisions(ytc_posX, ytc_posY, arrayVideos, settings)==0) {
							var videoType = [ytc_posX, ytc_posY, settings.videoWidth, settings.videoWidth*settings.proportion];
							arrayVideos.push(videoType);
							ytc_exit = 1;
						} else {
							ytc_attempts++;
						}
					}
				}
				// END CALCULATE POSITIONS
				
				$(this).parent().prepend("<div class='ytc_video' id='ytc_video" + numVideos + "' style='position:absolute;top:" + ytc_posY + "px;left:" + ytc_posX + "px;background-color:" + settings.borderColor + " !important;border:" + settings.borderSize + "px " + settings.borderStyle + " " + settings.borderColor + ";width:" + settings.videoWidth + "px;height:" + Math.round(settings.videoWidth * settings.proportion) + "px;'></div>");
				$("#ytc_video" + numVideos).append(divVideo);
				//alert(swfobject);
				swfobject.embedSWF("http://www.youtube.com/apiplayer?enablejsapi=1&version=3&playerapiid="+playerID,
	                        divID, settings.videoWidth, settings.videoWidth*settings.proportion, "8", null, null, params, atts);
			
	            numVideos++;
            	
			});
			
			$(".ytc_video").mouseenter(function() {
				var auxID = $(this).find("object").attr("id");
				ytplayer = document.getElementById(auxID);
				var elem = $(this);
				var elemTop = $(this).css("top").replace("px","");
				var elemLeft = $(this).css("left").replace("px","");
				if (!this.animObj) { this.animObj = { size:0, top:$(elem).css("top").replace("px",""), left:$(elem).css("left").replace("px","") } }
				$(this.animObj).stop().animate({
							size:100
						},{
							duration:settings.speed,
							step:function(now,fx){
									ytc_mute_all_videos();
									$(elem).css({zIndex:1000,top:Math.floor(elemTop/1-now/2),left:Math.floor(elemLeft/1-now/2),width:settings.videoWidth+now*settings.grow,height:Math.round(settings.videoWidth*settings.proportion)+now*settings.grow*settings.proportion}).find("object").attr("width", settings.videoWidth+now*settings.grow).attr("height", Math.round(settings.videoWidth*settings.proportion)+now*settings.grow*settings.proportion).css("zIndex",1000);
									ytplayer.setVolume(now);
									ytplayer.playVideo();
								},
							complete:function() {
								
							}
						});
			}).mouseleave(function() {
				var elem = $(this);
				var elemTop = this.animObj.top;
				var elemLeft = this.animObj.left;
				var auxID = $(this).find("object").attr("id");
				ytplayer = document.getElementById(auxID);
				$(this.animObj).stop().animate({
							size:0
						},{
							duration:settings.speed,
							step:function(now,fx){
									$(elem).css({zIndex:900,top:Math.floor(elemTop/1-now/2),left:Math.floor(elemLeft/1-now/2),width:settings.videoWidth+now*settings.grow,height:Math.round(settings.videoWidth*settings.proportion)+now*settings.grow*settings.proportion}).find("object").attr("width", settings.videoWidth+now*settings.grow).attr("height", Math.round(settings.videoWidth*settings.proportion)+now*settings.grow*settings.proportion).css("zIndex",900);
									if (settings.pause) { ytplayer.pauseVideo(); }
									ytplayer.setVolume(now);
								},
							complete:function() {
								
							}
						});
			});

		});
	};
})(jQuery);