<?php

function paginator($total_pages, $current_page, $window_size, $indicator=0) {
  /*
	html paginator helper
  */
	$start = $current_page - intval($window_size / 2);
	if ($start < 1) {
		$start = 1;
  }
	$end = $start + $window_size - 1;
	if ($end > $total_pages) {
		$start = max(1, $start - ($end - $total_pages));
		$end = $total_pages;
  }
	$ret = range($start, $end);
  print_r($ret);
	# insert indicator
	if ($ret[0] != 1) {
		$ret[0] = 1;
    array_splice($ret, 1, 0, $indicator);
  }
	if (end($ret) != $total_pages) {
    array_splice($ret, count($ret) - 1, 1, array($indicator, $total_pages));
  }
	return $ret;
}

# [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 100]
print_r(paginator(100, 2, 10));
# [1, 0, 15, 16, 17, 18, 19, 20, 21, 22, 0, 100]
print_r(paginator(100, 19, 10));
