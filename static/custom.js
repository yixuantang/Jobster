
$.fn.actionButton = function(o){
	$(this).click(function() {
		var $this = $(this);

		if($this.hasClass('fired'))
			return false; // only trigger once

	    $.post($this.attr('href'))
	    	.done(function(data){
		    	// success!
				console.log(data);

				var state = $this.data('next') || 'success'
				$this.data('state', state)

				if($this.data(state))
					$this.text($this.data(state));
				$this.addClass('special').addClass('fired');
			})
			.fail(function(data){});

	    return false;
	});

	$(this).filter(function(){
		return $(this).data('state');
	}).addClass('special').addClass('fired').each(function(){
		$(this).text($(this).data($(this).data('state'))); 
	});
}

window.isActive = true;
$(window).focus(function() { this.isActive = true; });
$(window).blur(function() { this.isActive = false; });


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


	$('.action').actionButton();





	function createMessage(who, message, status, timestamp) {
		var cell = $('<div>').attr('class', 'message-cell ' + who);
    	var message = $('<span>').attr('class', 'message')
    		.attr('title', timestamp)
    		.data('timestamp', timestamp)
    		.text(message);

    	if(status === 0)
    		cell.addClass('unread')

    	return cell.append(message);
	}

	function getNewMessages() {
		var last_timestamp = $('.messages .message:last').data('timestamp');
		console.log(last_timestamp)
		$.get($('.messages').data('get-messages'), {
			date: last_timestamp
		}).done(function(data){
	    	// success!
			console.log(data);

			if(data.messages) {
				data.messages.reverse().forEach(function(d){
					var message = createMessage('you', d.mtext, d.mstatus, d.mdate);
					$('.message-wrap').append(message);
				})

				sortMessages();
				keepAtBottom();
			}
		})
	}


	function sortMessages() {
		$('.messages-wrap').sort(function(a, b) {
			return $(a).find('.message').data('timestamp') > $(b).find('.message').data('timestamp');
		}).appendTo('.messages-wrap');
	}


	$('.new-message').on('keyup', function(e){
	    if(e.keyCode == 13 && $(this).val() != '') { // on enter key
	    	getNewMessages();
	    	var my_message = createMessage('me', $(this).val());
	        $('.message-wrap').append(my_message);

	        

	        $.post($(this).data('send-url'), {
	        	message: $(this).val()
	        }, function(data){
				
				my_message.find('.message')
					.attr('title', data.timestamp)
					.data('timestamp', data.timestamp)
				sortMessages();
	        	keepAtBottom();
			})

			$(this).val('')
	    }
	});

	// get new messages when refresh is clicked
	$('.messages .refresh').on('click', function(){
		getNewMessages();
	});

	// mark as read when the messages box (the entire messages section) is clicked
	$('.messages').on('click', function(){
		$(this).find('.messages.unread').each(function(){
			$this = $(this);
			$.post($(this).data('mark-read')).done(function(){
				$this.removeClass('unread');
			})
		})
	})

	// get new nessages every 5 seconds
	if($('.messages').length) {
		setInterval(function(){
			if (window.isActive) {
			    getNewMessages();
			}
		}, 8000)
	}
	

	// keep messages scrolled to bottom
	function keepAtBottom() {
		var el = $('.messages .double-wrap')
		if(stick && el.length) 
			el.scrollTop(el[0].scrollHeight);
	}

	// 
	var stick = true;
	keepAtBottom();
	$('.messages .double-wrap').on('scroll', function(){
		stick = $('.messages .double-wrap').scrollTop() + $('.messages .double-wrap').height() > $('.messages .message-wrap').height() - 10;

		keepAtBottom();
	})


})

