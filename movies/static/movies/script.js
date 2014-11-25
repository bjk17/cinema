$( document ).ready(function() {
//eitthvað hér? ef ekki þá eyða út
});

$("#chooseTheater").on("click", function() {
	$( "#theaterList" ).toggleClass( "hidden" );
});

$( document ).on("click", "#movies .movie .showShowtimes", function() {
    var element = $(this).closest(".movie").detach();
    $("#toSee").append(element);
});

$( document ).on("click", "#toSee .movie .showShowtimes", function() {
    var element = $(this).closest('.movie').detach();
    $("#movies").append(element);
});



//$('#toSee:empty').hide();
/*
pæling til að fela tómt div
$('#australopithecus #homo-sapiens').length // Should be 1
$('#homo-sapiens #homo-herectus').length // Should be 0
*/