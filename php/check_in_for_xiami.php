<?php
// see ../python/py-tools for a GAE version

error_reporting(E_ALL);
$x = curl_init('http://www.xiami.com/task/signin');
curl_setopt($x, CURLOPT_HTTPHEADER, array(
    'Accept:application/json, text/javascript, */*',
    'Accept-Language: zh-cn,zh;q=0.5',
    'Accept-Encoding: deflate',
    'Accept-Charset:UTF-8,*;q=0.5',
    'Content-Length: 0',
    'Content-Type: application/xml',
    'Referer: http://www.xiami.com/',
    'X-Requested-With: XMLHttpRequest',
));
curl_setopt($x, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12');
curl_setopt($x, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($x, CURLOPT_POST, 1);
curl_setopt($x, CURLOPT_COOKIE, 'auth=abcd');
var_dump(curl_exec($x));
curl_close($x);
