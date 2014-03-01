$(function () {
	var $temp = $(".temp"),
		$body = $("body");
	setInterval(function () {
		$.getJSON($SCRIPT_ROOT + '/update', function (data) {
     	   $temp.text(data.temp);
     	   $body.removeClass().addClass(data.klass);
	    });
	}, 1000);
});
