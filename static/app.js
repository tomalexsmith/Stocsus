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
        var supplier_name = $(this).attr('supplier_name');



        req = $.ajax({
            url : '/update_favourite',
            type : 'POST',
            data : { supplier_name : supplier_name }
        });

        req.done(function() {

        // $(".fav_supplier.fav_supplier='\" + supplier_name+ "']").html("Testing button");

            $(".fav_btn").html("❤");
            $(".table__row").fadeOut(1000).fadeIn(1000);

    });
  });
      $('.blacklist_supplier').on('click', function() {
        var supplier_name = $(this).attr('supplier_name');
        req = $.ajax({
            url : '/update_blacklist',
            type : 'POST',
            data : { supplier_name : supplier_name }
        });
        req.done(function() {
              $('.blacklist_supplier').fadeOut(1000).fadeIn(1000);
              $(".blacklist_btn").html("Successfully blacklisted, will not be displayed on next search");
    });
  });
});







