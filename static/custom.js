$(document).ready(function(){




	$('.notification.unread').on('click', function(){
		var $this = $(this);
		$.post($(this).find('.action.mark-read').attr('href'), function(data){
			// success!
			console.log(data);
			$this.removeClass('unread');
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


	function createMessage(who, message, timestamp, status) {
		var cell = $('<div>').attr('class', 'message-cell ' + who);
    	var message = $('<span>').attr('class', 'message')
    		.attr('title', timestamp)
    		.data('timestamp', timestamp)
    		.text(message);

    	if(status)
    		cell.addClass('unread')

    	return cell.append(message);
	}

	function getNewMessages() {
		var placeholder = $('<div>');
		$('.message-wrap').append(placeholder);

		$.get($('.messages').data('get-messages'), {})
	    	.done(function(data){
		    	// success!
				console.log(data);

				if(data.messages) {
					data.messages.reverse().forEach(function(d){
						var message = createMessage('you', d.mtext, d.mtime, d.mstatus);
						$(placeholder).after(message);
					})
					placeholder.remove();
				}
			})
	}


	$('.new-message').on('keyup', function(e){
	    if(e.keyCode == 13) { // on enter key
	    	var timestamp = $(this).closest('.messages').select('.message:last').data('timestamp');


	    	getNewMessages();
	    	var my_message = createMessage('me', $(this).val());
	        $('.message-wrap').append(my_message);


	        $.post($(this).data('send-url'), {
	        	message: $(this).val(),
	        	timestamp: timestamp
	        }, function(data){
				
			})

			$(this).val('')
	    }
	});

	$('.messages .refresh').on('click', function(){
		getNewMessages();
	})


	setTimeout(function(){
		getNewMessages();
	}, 15000)



})

