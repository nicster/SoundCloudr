$.getJSON('/tracks', function(tracks){
    $(function() {

        var widgetIframe = document.getElementById('sc-widget');
        widgetIframe.src = 'https://w.soundcloud.com/player/?url=http://api.soundcloud.com/tracks/' + tracks[0];
        var widget       = SC.Widget(widgetIframe),
            position     = 0;

        widget.bind(SC.Widget.Events.PLAY_PROGRESS, function(play_progress) {
            if (play_progress.relativePosition > 0.999) {
                skip();
            }
        });

        $('#next').click(function() {
            skip();
            $('#error').empty();
        });

        $('#last').click(function() {
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
                widget.load('http://api.soundcloud.com/tracks/' + tracks[position], {
                    auto_play: true,
                    buying: false
                });
            }
            else {
                $('#content').html("<div id='done'>come back later for more</dive>");
            }
        }

        function last() {
            position -= 1;
            if (position >= 0) {
                widget.load('http://api.soundcloud.com/tracks/' + tracks[position], {
                    auto_play: true,
                    buying: false
                });
            }
            else {
                $('#error').empty();
                $('#error').append("<div id='error'>Can't go back. This is the last track</div>");
            }
        }
    });
});
