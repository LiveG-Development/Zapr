// @import https://code.jquery.com/jquery-3.4.1.min.js

var dom = {
    jQuery: window.jQuery,
    loaded: function(callback) {
        this.jQuery(callback);
    }
};

delete jQuery;