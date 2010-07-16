<?php
// not working
error_reporting(E_ALL);
$x = curl_init('http://www.xiami.com/task/signin');
curl_setopt($x, CURLOPT_HTTPHEADER, array(
    'Host: www.xiami.com',
    'User-Agent: Mozilla/5.0 (X11; U; Linux i686; zh-CN; rv:1.9.2.6) Gecko/20100628 Ubuntu/10.04 (lucid) Firefox/3.6.6',
    'Accept: */*',
    'Accept-Language: zh-cn,zh;q=0.5',
    'Accept-Encoding: deflate',
    'Accept-Charset: GB2312,utf-8;q=0.7,*;q=0.7',
    'Keep-Alive: 115',
    'Connection: keep-alive',
    'X-Requested-With: XMLHttpRequest',
    'Referer: http://www.xiami.com/',
    'Content-Length: 0',
    'Content-Type: text/plain; charset=UTF-8',
    'Cookie: ' . file_get_contents('/home/yc/xiami.cookie'),
    'Pragma: no-cache',
    'Cache-Control: no-cache',
));
curl_setopt($x, CURLOPT_POST, 1);
//curl_setopt($x, CURLOPT_HEADER, 1);
curl_setopt($x, CURLOPT_RETURNTRANSFER, 1);
echo curl_exec($x);
curl_close($x);
