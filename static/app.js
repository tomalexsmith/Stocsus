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
            // $('.updateButton').fadeOut(1000).fadeIn(1000);



            // $('#memberNumber'+member_id).text(data.member_num);
    });
  });
});


