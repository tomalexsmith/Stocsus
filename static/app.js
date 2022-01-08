$(document).ready(function() {

    $('.add_watchlist').on('click', function() {
        var i = $(this).attr('i');


        req = $.ajax({
            url : '/update_watchlist',
            type : 'POST',
            data : { part_number : i }
        });

        req.done(function() {
            $('.add_watchlist').fadeOut(1000).fadeIn(1000);
            $(".watchlist_btn").html("Successfully Added");
    });
  });

     $('.fav_supplier').on('click', function() {
        var i = $(this).attr('i');


        req = $.ajax({
            url : '/update_favourite',
            type : 'POST',
            data : { supplier_name : i }
        });

        req.done(function() {
            $('.fav_supplier').fadeOut(1000).fadeIn(1000);
            $(".fav_btn").html("❤");
            $(".table__row").fadeOut(1000).fadeIn(1000);

    });
  });
      $('.blacklist_supplier').on('click', function() {
        var i = $(this).attr('i');
        req = $.ajax({
            url : '/update_blacklist',
            type : 'POST',
            data : { supplier_name : i }
        });
        req.done(function() {
              $('.blacklist_supplier').fadeOut(1000).fadeIn(1000);
              $(".blacklist_btn").html("Successfully blacklisted, will not be displayed on next search");
    });
  });
});




$(document).ready(function() {
$('.flight_button').on('click', function() {
        var i = $(this).attr('flight_number');
        req = $.ajax({
            url : '/add_flight_number',
            type : 'POST',
            data : { flight_number : flight_number }
        });

           req.done(function() {
               $(".flight_button").html("Successfully Added");

        });
      });
    });



