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
        });

        $('#logout').click(function() {
            $.get('/logout', function(data) {
                location.href="/";
            });
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
                $.get('/done', function(data) {
                    $('#content').html(data);
                });
            }
        }
    });
});
