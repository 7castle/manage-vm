$(document).ready(function() {
  $('#request_btn').click(function() {
    $('#myModal').modal('toggle');
    $('<input>').attr('type','hidden').attr('name','_request').attr('value','_request').appendTo('#vmForm');
    $('#vmForm').submit();
  });
});
