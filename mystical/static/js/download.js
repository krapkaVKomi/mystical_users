
$(document).ready(function() {
  // Attach a click listener to all download buttons (static and dynamic)
  $(document).on('click', 'a[id^="download-button-"]', function() {
    // Get the file ID from the button ID
    var file_id = $(this).attr('id').split('-')[2];

    // Send an AJAX request to the download view
    $.ajax({
      url: '/download-file/' + file_id + '/',
      method: 'GET',
      xhrFields: {
        responseType: 'blob'
      },
      success: function(data) {
        var blob = new Blob([data], {type: 'text/csv'});
        var link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = 'file_name.csv';  // Change the extension to .csv
        link.click();
      },
      error: function(xhr, status, error) {
        console.log('Error: ' + error);
      }
    });
  });
});




