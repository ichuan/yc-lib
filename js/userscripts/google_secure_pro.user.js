// Google Secure Pro
// version 1.4
// 2006-10-13
//
// --------------------------------------------------------------------
//
// This is a Greasemonkey user script.
//
// To install, you need Greasemonkey: http://greasemonkey.mozdev.org/
// Then restart Firefox and revisit this script.
// Under Tools, there will be a new menu item to "Install User Script".
// Accept the default configuration and install.
//
// To uninstall, go to Tools/Manage User Scripts,
// select "Google Secure Pro", and click Uninstall.
//
// --------------------------------------------------------------------
//
// ==UserScript==
// @name          Google Secure Pro
// @description   Forces gMail, gCal, Google Docs & Spreadsheets, and Google Reader to use secure connection.
// @include       http://mail.google.com/*
// @include       http://www.google.*/calendar/*
// @include       http://docs.google.*/*
// @include       http://spreadsheets.google.*/*
// @include       http://www.google.*/reader/*
// @include       http://www.google.*/bookmarks/*
// @include       http://www.google.*/history/*
// @include       http://groups.google.*/*
// @include       http://sites.google.*/*
// @include       http://knol.google.*/*
// @include       http://www.google.*/notebook/*
// @include       http://www.google.*/webmasters/*
// @include       http://www.google.*/contacts
// @include       http://www.google.*/voice/*
// @include       http://www.google.*/

// ==/UserScript==

var url = window.location.href;
window.location.replace(url.replace(url.substring(0,7), 'https://'));
