// 从 arr 数组中取 m 个元素组成一个新数组，调用 callback 处理
// 也就是数学里的组合
Array.prototype.forEach || (Array.prototype.forEach = function(callback){
	for (var i = 0, j = this.length; i < j; i++)
		callback(this[i], i);
});
function combination(arr, m, callback){
	n = arr.length;

	if (m == 1){
		arr.forEach(function(val){
			callback([val]);
		});
		return;
	}

	if (n <= m){
		callback(arr.slice());
		return;
	}

	for (var i = 0, j = n - m + 1; i < j; i++)
		combination(arr.slice(i + 1), m - 1, function(arr2){
			arr2.unshift(arr[i]);
			callback(arr2);
		});
}
