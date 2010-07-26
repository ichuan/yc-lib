<?php
// source: http://coolshell.cn/?p=2704

// 1. 判断质数
function isPrime($i)
{
    $str = str_repeat('1', $i);
    return !preg_match('/^1?$|^(11+?)\\1+$/', $str);
}

for($i = 0; $i < 1000; $i++)
    if(isPrime($i))
        echo $i, ' ';

echo "\n";

// 2. 解方程: 17x + 12y = 51
if (preg_match('/^(.*)\\1{16}(.*)\\2{11}$/', str_repeat(',', 51), $m))
    echo sprintf("x = %d, y = %d\n", strlen($m[1]), strlen($m[2]));
