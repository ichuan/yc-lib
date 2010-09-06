<?php
$n = 6;
$m = array(2,3,4,5,6);

$nn = array_fill(0,$n,0);
$nn[0] = 1;
$nnn = array_fill(0, $n, 9);
//for (){
//    ;
//}

function num($arr){
    $r = 0;
    for ($x = count($arr), $y = array_shift($arr); $y !== NULL; $x--){
        $r += $y * pow(10, $x - 1);
        $y = array_shift($arr);
    }
    return $r;
}
$x = 65432;
$y = '' . $x;
var_dump(str_split($y));
