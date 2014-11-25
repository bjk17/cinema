/*$( document ).ready(function() {
//eitthvað hér? ef ekki þá eyða út
});


$("div#chooseTheater").click(function() {
	$( "ul#theaterList" ).toggleClass( "hidden" );
});

$(".showShowtimes").click(function() {
	alert("yess");
    var element = $(this).closest('.movie').detach();
    alert(element);
    if 
    $('#movies').append(element);
});*/

$( document ).on("click", "#movies .movie .showShowtimes", function() {
	console.log("movies");
    var element = $(this).closest('.movie').detach();
    $('#toSee').append(element);
});

$( document ).on("click", "#toSee .movie .showShowtimes", function() {
	console.log("toSee");
    var element = $(this).closest('.movie').detach();
    $('#movies').append(element);
});



//$('#toSee:empty').hide();
/*
pæling til að fela tómt div
$('#australopithecus #homo-sapiens').length // Should be 1
$('#homo-sapiens #homo-herectus').length // Should be 0
*/