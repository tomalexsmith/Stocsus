$(document).ready(function() {

    $('.updateButton').on('click', function() {
        var i = $(this).attr('i');


        req = $.ajax({
            url : '/update_watchlist',
            type : 'POST',
            data : { part_number : i }
        });

        req.done(function(data) {
            $('.updateButton').fadeOut(1000).fadeIn(1000);
            // $('#memberNumber'+member_id).text(data.member_num);

    });


  });

});


