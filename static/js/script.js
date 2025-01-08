$(document).ready(function() {
    $('#upload-form').on('submit', function(event) {
        event.preventDefault();

        var formData = new FormData(this);
        $.ajax({
            url: '/predict',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                $('#predicted-class').text(response.class);
                $('#confidence').text((response.confidence * 100).toFixed(2));
                $('#result').fadeIn();
            },
            error: function() {
                alert('Error uploading image. Please try again.');
            }
        });
    });
    $('#title-classes').on('click', function() {
        $('#classes-list').toggle();  // This will toggle the visibility of the class list
    });
});
