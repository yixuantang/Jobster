
$('.notification.unread').on('click', function(){
	$.post($(this).find('.action.mark-read').attr('href'), function(data){
		// success!
		console.log(data);
		$(this).removeClass('unread');
	})
	
	return false;
});



// $('.action.friend-request').click(function() {
// 	var $this = $(this);

// 	if($this.hasClass('special'))
// 		return false; // only trigger once

//     $.post($this.attr('href'), function(data){
//     	// success!
// 		console.log(data);
// 		$this.text($this.data('success')).addClass('special');
// 	});
//     return false;
// });


$('.action').click(function() {
	var $this = $(this);

	if($this.hasClass('fired'))
		return false; // only trigger once

    $.post($this.attr('href'), function(data){
    	// success!
		console.log(data);
		$this.text($this.data('success')).addClass('special').addClass('fired');
	});


    return false;
});