$(function () {
    $('.exchange_submit').click(function () {
      var postData = {
        "money": $('.money').val(),
        "currency": $('select[name="exchange_rate_form"]').val()
      }
      console.log(postData);
      $.ajax({
        url: "/exchange_money_ajax",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(postData),
        success: function (data) {
            var money = data["result"];
            var rate = data["rate"];
            document.getElementById('exchange_result').innerHTML = `<p>價值台幣 ${money} 元</p>`;
            document.getElementById('exchange_rate').innerHTML = `<p>匯率 ${rate} 元</p>`;
        }
      });
    });
  });