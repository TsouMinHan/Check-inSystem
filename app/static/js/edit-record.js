function ajax_data(checked, student_id, date, course_name, student_name){

    var postData = {
                    "checked": checked,
                    "student_id": student_id,
                    "date": date,
                    "course_name": course_name,
                    "student_name": student_name
                  };

    $.ajax({
      url: "/edit_record_ajax",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify(postData),
      success: function (data) {
        alert(data.result);
        document.location.reload;
      }
    });
};

$(function () {
    $('input:button').click(function () {
      var input_id = $(this).attr("id");
      var checked = document.getElementById("checkbox"+input_id).checked;
      var student_id = document.getElementById("student_id"+input_id).textContent;
      var date = document.getElementById("date"+input_id).textContent;
      var course_name = document.getElementById("course_name"+input_id).textContent;
      var student_name = document.getElementById("student_name"+input_id).textContent;
      
      ajax_data(checked, student_id, date, course_name, student_name);
      console.log("check"+input_id ,"student_id"+input_id, "date"+input_id);
    });
});