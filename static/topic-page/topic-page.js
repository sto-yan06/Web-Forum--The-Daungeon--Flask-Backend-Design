$(document).ready(function () {
    // Add an event listener to the close button or a close action trigger
    $("#close-thread-button").on("click", function () {
        $.ajax({
            type: "POST", // Set the HTTP method to POST
            url: closeThreadUrl, // Use the JavaScript variable here
            success: function (response) {
                if (response.success) {
                    // Display a pop-up message with the success message
                    alert(response.message);
                    // You can also update the page content if needed
                    // Example: $("#thread-status").text("Thread closed");

                    // Redirect back to the topic page
                    window.location.href = redirectURL;
                } else {
                    // Display a pop-up message with the error message
                    alert(response.message);
                }
            },
            error: function () {
                alert("An error occurred while processing your request.");
            }
        });
    });
});


var threadStatus = document.getElementById('thread-status');
if(threadOpened == 0){
    threadStatus.style.backgroundColor = '#FF0000' 
} 
else{
    threadStatus.style.backgroundColor = '#4CAF50'
}