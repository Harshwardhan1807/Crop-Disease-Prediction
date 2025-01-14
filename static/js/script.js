$(document).ready(function() {
    $('#upload-form').on('submit', function(event) {
        event.preventDefault();

        var formData = new FormData(this); // Create a formdata onject from the given form
        var fileInput = $('#file-upload')[0].files[0]; // Get the uploaded file

        if (fileInput) {
            // Displaying the uploaded image
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#uploaded-image').attr('src', e.target.result).show();
            };
            reader.readAsDataURL(fileInput); 
        }
        // Send the form data to the server
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
    // Toggle the visibility of the class list when title is clicked
    $('#title-classes').on('click', function() {
        $('#classes-list').toggle();  
    });
});
