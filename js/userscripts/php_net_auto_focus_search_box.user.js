// ==UserScript==
// @name           php_net_auto_focus_search_box
// @namespace      php
// @include        http://*php.net/*
// @author         yc@2009-10-27 11:48:26
// ==/UserScript==

var $ = function (id) { return (typeof(id) == 'object') ? id : document.getElementById(id); }
var $$ = function (id, tag) { return $(id).getElementsByTagName(tag); }

if ($('headsearch')){
    var i = $$('headsearch', 'input');
    try {i[0].focus();} catch(e) {}
}  
