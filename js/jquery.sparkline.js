/**
 * jQuery sparkline chart plugin
 * draw sparkline using canvas, need excanvas support in IE9-
 * demo: http://ichuan.net/static/sparkline.html
 *
 * @author yc <iyanchuan@gmail.com>
 */
(function($){
	$.fn.sparkline = function(options){
		options || (options = {});
		options = $.extend({
			color: '#058DC7',
			lineWidth: 1.1
		}, options);

		return this.each(function(){
			var el = $(this), opts = $.extend({}, options), cls = el[0].className;
			var height = el.height(), width = el.width();
			$.each(['color', 'numbers', 'lineWidth'], function(_, item){
				var value = el.data(item);
				if (value !== undefined)
					opts[item] = value;
			});
			if ($.type(opts.numbers) === 'string')
				opts.numbers = $.map(opts.numbers.split(','), function(i){ return parseInt(i, 10); });

			var min = Math.min.apply(null, opts.numbers),
				max = Math.max.apply(null, opts.numbers);
			var vGap = max - min, hGap = ~~(width / opts.numbers.length), offsetY = 0, multiply = 1;
			if (vGap >= height){
				multiply = height / vGap;
				offsetY = ~~(max * multiply - height);
			} else
				offsetY = ~~(min - (height - vGap) / 2);

			var new_el = document.createElement('canvas');
			new_el.setAttribute('width', width);
			new_el.setAttribute('height', height);
			if (cls)
				new_el.setAttribute('class', cls);
			window.G_vmlCanvasManager && G_vmlCanvasManager.initElement(new_el);
			if (!new_el.getContext)
				return;
			el.replaceWith(new_el);

			var ctx = new_el.getContext('2d');
			ctx.lineWidth = parseFloat(opts.lineWidth);
			ctx.lineJoin = 'round';
			ctx.beginPath();
			var first = true;
			for (var i = 0, j = opts.numbers.length; i < j; i++){
				var x = ~~(hGap * i), y = height - ~~(opts.numbers[i] * multiply - offsetY);
				if (first){
					ctx.moveTo(x, y);
					first = false;
				} else
					ctx.lineTo(x, y);
			}
			ctx.strokeStyle = opts.color;
			ctx.stroke();
		});
	};
})(jQuery);
