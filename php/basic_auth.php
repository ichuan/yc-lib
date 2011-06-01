<?php

$user = $_SERVER['PHP_AUTH_USER'];
$pass = $_SERVER['PHP_AUTH_PW'];

if ($user == 'yc' && $pass == 'yc')
	echo 'ok';
else {
   header('WWW-Authenticate: Basic realm="Secret"');
   header('HTTP/1.0 401 Unauthorized');
   echo 'Authorization Required.';
}
