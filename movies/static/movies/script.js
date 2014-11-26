$( document ).ready(function() {


    //eyða út?
    //haka við öll bíó
    //geyma fyrra val?
    updateMovies();
});

//dropdown for theaters
$("#chooseTheater").on("click", function() {
    $( "#theaterList" ).toggleClass( "hidden" );
});

//move movie to "my movies"
$( document ).on("click", "#movies .movie .moveMovie", function() {
    var element = $(this).closest(".movie").detach();
    $(this).text("Taka úr mínum myndum");
    $("#toSee").append(element);
});

//move movie back to "all movies"
$( document ).on("click", "#toSee .movie .moveMovie", function() {
    var element = $(this).closest('.movie').detach();
    $(this).text("Bæta við mínar myndir");
    $("#movies").append(element);
});

//Returns the user preferred theaters
function getSelectedTheaters (x,y) {
    var checkedValues = $(".theater:checked").map(function() {
        return this.value;
    }).get();
    return checkedValues;
};

//shows movies based on user's choice of theaters
function updateMovies() {
    var theaters = getSelectedTheaters();
    $(".movie").each( function(j, movie){
        //~ Er buggy, virkar ekki hjá Bjarna
        // $(movie).hide();
    });
    jQuery.each( theaters, function(i, theater) {
        console.log(i+theater);
        $(".movie").each( function(j, movie){
            if($(movie).hasClass(theater)){
                $(movie).show();
                //fela allar fyrst?
                //birta mynd
                //birta sýningartíma fyrir það bíó
            }
        });
    });
};

//listens to changes in user theater choice
$( "input:checkbox" ).change(function() {
    
    updateMovies(theaters);
    console.log(theaters);
});

/*
$(this).val();
Or if you have set a class or id for it, you can:

$('#check_id').val();
$('.check_class').val();
Also you can check whether it is checked or not like:

if ($('#check_id').is(":checked"))
{
  // it is checked
}

//$('#toSee:empty').hide();
/*
pæling til að fela tómt div
$('#australopithecus #homo-sapiens').length // Should be 1
$('#homo-sapiens #homo-herectus').length // Should be 0
*/