<?php
// source: http://coolshell.cn/?p=2704

function isPrime($i)
{
    $str = str_repeat('1', $i);
    return !preg_match('/^1?$|^(11+?)\\1+$/', $str);
}

for($i = 0; $i < 1000; $i++)
    if(isPrime($i))
        echo $i, ' ';
