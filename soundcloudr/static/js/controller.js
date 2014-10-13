$.getJSON('/tracks', function(tracks){
    $('#last1').show(500);
    $('#next1').show(500);
    $('#hdashboard').show(500);
    $(function() {

        var widgetIframe = document.getElementById('sc-widget1');
        widgetIframe.src = 'https://w.soundcloud.com/player/?url=http://api.soundcloud.com/tracks/' + tracks[0];
        var widget1       = SC.Widget(widgetIframe),
            likeposition = 0,
            position     = 0;

        widget1.bind(SC.Widget.Events.PLAY_PROGRESS, function(play_progress) {
            if (play_progress.relativePosition > 0.999) {
                skip();
            }
        });

        $('#next1').click(function() {
            skip();
            $('#error1').empty();
        });

        $('#last1').click(function() {
            last();
        });

        $('#logout').click(function() {
            $.get('/logout', function(data) {
                location.href="/";
            });
        });

        $('#logo').click(function() {
            location.href="/";
        });

        function skip() {
            $.post('/playposition', {last_played: tracks[position]});
            position++;
            if (tracks[position]) {
                widget1.load('http://api.soundcloud.com/tracks/' + tracks[position], {
                    auto_play: true,
                    buying: false
                });
            }
            else {
                $('#content').html("<div id='done'>come back later for more</dive>");
            }
        }

        function last() {
            if (position-1 >= 0) {
                position -= 1;
                widget1.load('http://api.soundcloud.com/tracks/' + tracks[position], {
                    auto_play: true,
                    buying: false
                });
            }
            else {
                $('#error1').empty();
                $('#error1').append("Can't go back. This is the last track");
            }
        }

        $.getJSON('/likes', function(likes) {
            $('#last2').show(500);
            $('#next2').show(500);
            $('#hlikes').show(500);
            var widgetIframe = document.getElementById('sc-widget2');
            shuffle(likes);
            widgetIframe.src = 'https://w.soundcloud.com/player/?url=http://api.soundcloud.com/tracks/' + likes[0];
            var widget2      = SC.Widget(widgetIframe);

            widget2.bind(SC.Widget.Events.PLAY_PROGRESS, function(play_progress) {
                if (play_progress.relativePosition > 0.999) {
                    skiplike();
                }
            });

            $('#next2').click(function() {
                skiplike();
                $('#error2').empty();
            });

            $('#last2').click(function() {
                lastliked();
            });

            function skiplike() {
                likeposition++;
                if (likes[likeposition]) {
                    widget2.load('http://api.soundcloud.com/tracks/' + likes[likeposition], {
                        auto_play: true,
                        buying: false
                    });
                }
                else {
                    $('#content').html("<div id='done'>come back later for more</dive>");
                }
            }

            function lastliked() {
                if (likeposition-1 >= 0) {
                    likeposition -= 1;
                    widget2.load('http://api.soundcloud.com/tracks/' + likes[likeposition], {
                        auto_play: true,
                        buying: false
                    });
                }
                else {
                    $('#error2').empty();
                    $('#error2').append("Can't go back. This is the last track");
                }
            }
        });

        function shuffle(o){ //v1.0
            for(var j, x, i = o.length; i; j = Math.floor(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
            return o;
        }
    });
});
