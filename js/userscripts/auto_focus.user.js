// ==UserScript==
// @name           auto_focus
// @namespace      php
// @include        http://*
// @include        https://*
// @description    press ` to switch focus between inputable areas
// @author         yc@2009
// ==/UserScript==

//var inputs = document.getElementsByTagName('input');
var inputs = unsafeWindow.document.evaluate('//input[@type="text"] | //textarea | //input[@type="password"] | //input[not(@type)]', unsafeWindow.document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null);
var i = 0;
var preInput = null;

function focusNext(e)
{
    if (e && e.keyCode == 192){
        if (preInput){
            preInput.style.border = preInput.getAttribute('__border');
            preInput.value = preInput.value.replace(/`$/, '');
        }
        var j = inputs.snapshotItem(i);
        preInput = j;
        if (!j.getAttribute('__border'))
            j.setAttribute('__border', j.style.border);
        j.style.border = '1px solid red';
        var jsObj = j.wrappedJSObject || j;
        jsObj.scrollIntoView();
        j.focus();
        j.value = j.value.replace(/`$/, '');
        if (++i >= inputs.snapshotLength)
            i = 0;
        e.returnValue = false;
        e.cancel = true;
    }
}
if (inputs.snapshotLength > 0)
    window.addEventListener('keyup', focusNext, true);
