$.getJSON('/tracks', function(tracks){
    $(function() {
        var widgetIframe = document.getElementById('sc-widget');
        widgetIframe.src = 'https://w.soundcloud.com/player/?url=http://api.soundcloud.com/tracks/' + tracks[0];
        var widget       = SC.Widget(widgetIframe),
            position     = 0;

        /*widget.bind(SC.Widget.Events.PLAY_PROGRESS, function(hallo) {
            console.log(hallo);
        });*/

        widget.bind(SC.Widget.Events.FINISH, function() {
            console.log('1');
            $.post('/playposition', {last_played: tracks[position]});
            console.log('2');
            position++;
            widget.load('http://api.soundcloud.com/tracks/' + tracks[position], {
                auto_play: true,
                buying: false
            });
        });
    });
});
