// ==UserScript==
// @name           auto-login-for-rsas
// @namespace      php
// @include        http*://*/user/requireLogin*
// @include        http*://*/user/logout*
// @author         yc
// ==/UserScript==
var $ = function(id){ return typeof(id)=='object' ? id : document.getElementById(id); };
var $$ = function(id,tag) { return $(id).getElementsByTagName(tag); };
try{
    if ($('username').value){
        $('loginForm').submit();
    } else {
        $('username').value="admin";
        $('password').value="nsfocus";
        $('username').select();
        $('loginForm').submit();
    }
    //setTimeout(function(){$('loginForm').submit();},500);
} catch (e){}
