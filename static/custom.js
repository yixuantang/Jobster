
$('.notification.unread').on('click', function(){
	$.post($(this).find('.action.mark-read').attr('href'), function(data){
		// success!
		console.log(data);
		$(this).removeClass('unread');
	})
	
	return false;
});


$('.action').click(function() {
	var $this = $(this);

	if($this.hasClass('fired'))
		return false; // only trigger once

    $.post($this.attr('href'))
    	.done(function(data){
	    	// success!
			console.log(data);

			if($this.data('success'))
				$this.text($this.data('success'));
			$this.addClass('special').addClass('fired');
		})
		.fail(function(data){});

    return false;
});







