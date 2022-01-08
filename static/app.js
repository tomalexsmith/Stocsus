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
            $(".add_watchlist").html("Successfully Added");
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
            $(".fav_btn").html("Successfully Added");

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
              $('.fav_supplier').fadeOut(1000).fadeIn(1000);
              $(".blacklist_btn").html("Successfully Added");
    });
  });
});


