$( document ).ready(function() {
  xalert("hello");
});


$("div#chooseTheater").click(function() {
	$( "ul#theaterList" ).toggleClass( "hidden" );
});

$('.showShowtimes').on('click', function() {
    var element = $(this).closest('.movie').detach();
    $('#toSee').append(element);
});

//$('#toSee:empty').hide();