// ==UserScript==
// @name           twitter_show_login
// @namespace      blog
// @include        https://twitter.com/
// @include        http://twitter.com/
// ==/UserScript==
var x = document.getElementById('signin_menu');
if (x)
    x.className='common-form standard-form ';
