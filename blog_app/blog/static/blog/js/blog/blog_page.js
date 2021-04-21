$(document).ready(function(){
    $('#add_comment').click(function(){
        var blog_id = $('#blog_container').data('id');
        var comment = $('#comment_box').val();
        $.ajax({
            url: '/blog/add_comment/',
            method: 'POST',
            data: {csrfmiddlewaretoken:$('[name="csrfmiddlewaretoken"]').val(),blog_id:blog_id,comment:comment},
            success: function(data){
                M.toast({html:'Comment added successfully!It will be displayed once its approved.'});
                $('#comment_box').val('');
            },
            error: function(error){
                M.toast({html:'Something went wrong.Please contact support.'})
            }
        });
    });

    $('.approve_comment').click(function(){
        var comment_id = $(this).closest('.comment_li').data('id');
        $.ajax({
            url: '/blog/approve_comment/',
            method: 'POST',
            data: {csrfmiddlewaretoken:$('[name="csrfmiddlewaretoken"]').val(),comment_id:comment_id},
            success: function(data){
                M.toast({html:'Comment approved successfully!'});
                $('.comment_actions').hide();
            },
            error: function(data){
                M.toast({html:'Something went wrong.Please contact support.'})
            }
        });
    });

    $('.reject_comment').click(function(){
        var comment_id = $(this).closest('.comment_li').data('id');
        $.ajax({
            url: '/blog/reject_comment/',
            method: 'POST',
            data: {csrfmiddlewaretoken:$('[name="csrfmiddlewaretoken"]').val(),comment_id:comment_id},
            success: function(data){
                M.toast({html:'Comment rejected successfully!'});
                $('.comment_li[data-id='+data+']').hide();
            },
            error: function(data){
                M.toast({html:'Something went wrong.Please contact support.'})
            }
        });
    });
});