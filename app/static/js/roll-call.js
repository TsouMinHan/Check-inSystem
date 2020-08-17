function ajax_data(){
    var inputs = document.getElementsByTagName("input");
    var postData = {};
    for(var i = 0; i < inputs.length; i++) {
        if(inputs[i].type == "checkbox") {
            postData[inputs[i].id] = inputs[i].checked;
        }
    }
    console.log(postData);
    $.ajax({
      url: "/record_ajax",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify(postData),
      success: function (data) {
        alert(data.result);
        document.location.href="/"
      }
    });
};

$(function () {
    $('#sent_to_record').click(function () {
      ajax_data();
    });
});