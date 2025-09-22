(function() {
    if (!window.bookmarklet) {
        var bookmarklet__js = document.body.appendChild(document.createElement('script'));
        bookmarklet__js.src = '//127.0.0.1:8000/static/js/bookmarklet.js?r='+Math.floor(Math.random()*9999999999999999);
        window.bookmarklet = true;
    } else {
        bookmarkletLaunch();
    }
})();

// This code check whether the bookmarklet has already been loaded by checking the value of the bookmarklet window var: with if(!window.bookmarklet): 