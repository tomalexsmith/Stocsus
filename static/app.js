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

     $(".fav_btn").on('click', function() {
        var supplier_name = $(this).attr('supplier_name');


        req = $.ajax({
            url : '/update_favourite',
            type : 'POST',
            data : { supplier_name : supplier_name }
        });

        req.done(function() {
            // fav button changes on click
            // blacklist button is removed on fav button click

            $(".fav_btn_"+supplier_name).fadeOut(1000).fadeIn(1000);
            $(".blacklist_btn_"+supplier_name).fadeOut(1000).fadeIn(1000);
            $(".blacklist_btn_"+supplier_name).remove()
            $(".fav_btn_"+supplier_name).html("❤");

    });
  });
      $('.blacklist_btn').on('click', function() {
        var supplier_name = $(this).attr('supplier_name');
        req = $.ajax({
            url : '/update_blacklist',
            type : 'POST',
            data : { supplier_name : supplier_name }
        });
        req.done(function() {
            // blacklist button changes on click
            // fav button is removed on blacklist button click
              $(".blacklist_btn_"+supplier_name).fadeOut(1000).fadeIn(1000);
              $(".fav_btn_"+supplier_name).fadeOut(1000).fadeIn(1000);
              $(".fav_btn_"+supplier_name).remove()
              $(".blacklist_supplier_"+supplier_name).html("Successfully blacklisted, will not be displayed on next search");
    });
  });
});

