function addActivity() {
    var activity = prompt('Enter an activity:'); // You can replace this with your own input method
    if (activity) {
        $.post('/add_activity', { activity: activity }, function (data) {
            alert(data);
        });
    }
}

function displayActivityLog() {
    $.get('/get_activity_log', function (data) {
        var activityLog = data;
        var activityLogList = $('#activity-log');
        activityLogList.empty();
        for (var i = 0; i < activityLog.length; i++) {
            var listItem = $('<li>').text(activityLog[i]);
            activityLogList.append(listItem);
        }
    });
}

$(document).ready(function () {
    displayActivityLog();
});