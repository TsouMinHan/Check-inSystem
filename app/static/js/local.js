//Get camera video
if (window.screen.width>1200){
    var constraints = {
        audio: false,
        video: {
            height: 960,
            width: 1280,
        }        
    };

    var window_form = "computer";
    document.getElementById("myVideo").style.webkitTransform = "scale(-1, 1)";

    document.getElementById("send_btn").style.width = `200px`;
    document.getElementById("send_btn").style.fontSize = `50px`;
    document.getElementById("send_div").style.bottom = `100px`;
    document.getElementById("send_div").style.left = `200px`;
}
else{
    var constraints = {
        audio: false,
        video: {
            height: 960,
            width: 1280,
            facingMode: {
                exact: "environment"
            }
        }        
    };

    var window_form = "phone";

    document.getElementById("send_btn").style.width = `200px`;
    document.getElementById("send_btn").style.fontSize = `50px`;
    document.getElementById("send_div").style.bottom = `100px`;
    document.getElementById("send_div").style.left = `250px`;
}



navigator.mediaDevices.getUserMedia(constraints)
    .then(stream => {
        document.getElementById("myVideo").srcObject = stream;
        console.log("Got local user video");

    })
    .catch(err => {
        console.log('navigator.getUserMedia error: ', err)
    });


