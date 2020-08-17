/**
 * Created by chad hart on 11/30/17.
 * Client side of Tensor Flow Object Detection Web API
 * Written for webrtcHacks - https://webrtchacks.com
 */

//Parameters
const s = document.getElementById('objDetect');
const sourceVideo = s.getAttribute("data-source");  //the source video to use
const uploadWidth = s.getAttribute("data-uploadWidth") || 640; //the width of the upload file
const mirror = s.getAttribute("data-mirror") || false; //mirror the boundary boxes
const scoreThreshold = s.getAttribute("data-scoreThreshold") || 0.5;
const apiServer = s.getAttribute("data-apiServer") || window.location.origin + '/image'; //the full TensorFlow Object Detection API server url
const className = s.getAttribute("data-title") || "";

let audio_arr = [];

//Video element selector
v = document.getElementById(sourceVideo);

//for starting events
let isPlaying = false,
    gotMetadata = false;

//Canvas setup

//create a canvas to grab an image for upload
let imageCanvas = document.createElement('canvas');
let imageCtx = imageCanvas.getContext("2d");

//create a canvas for drawing object boundaries
let drawCanvas = document.createElement('canvas');
document.body.appendChild(drawCanvas);
let drawCtx = drawCanvas.getContext("2d");

//draw boxes and labels on each detected object
function drawBoxes(objects) {

    //clear the previous drawings
    drawCtx.clearRect(0, 0, drawCanvas.width, drawCanvas.height);

    //filter out objects that contain a class_name and then draw boxes and labels on each
    objects.filter(object => object.person_name).forEach(object => {

        let x, y, width, height;
        console.log(window_form)
        // if (window_form=="phone"){
        //     x = object.x;
        //     y = object.y;
        //     width = (object.width) - x;
        //     height = (object.height) - y;
        // }
        // else if(window_form=="computer"){
        //     x = object.x;
        //     y = object.y;
        //     width = (object.width) - x;
        //     height = (object.height) - y;
        // }
        x = object.x;
        y = object.y;
        width = (object.width) - x;
        height = (object.height) - y;
        // document.getElementById("t").innerText=`${x}, ${y}, ${width}, ${height}`
        console.log(x, y, width, height, drawCanvas.width, drawCanvas.height);
        
        //flip the x axis if local video is mirrored
        // if (mirror) {
        if (window_form=="computer") {
            x = drawCanvas.width - (x + width)
        }
        console.log(object.check_threshold)
        if (object.second < 5){
            drawCtx.strokeStyle = "cyan";
            drawCtx.fillStyle = "cyan";
            drawCtx.fillText(object.person_name + " - " + (5-object.second), x + 5, y + 20);
        }            
        else{
            drawCtx.strokeStyle = "rgb(255,165,0)";
            drawCtx.fillStyle = "rgb(255,165,0)";
            drawCtx.fillText(object.person_name + "完成點名", x + 5, y + 20);
            if (object.student_id){
                audio_arr.push(object.student_id)
            }
            
            if (audio_arr.length>0){
                var source = document.getElementById('audio_source');
                source.src = `/static/audio/${audio_arr[0]}.mp3`;
                var playPromise = document.querySelector('audio')
                if (playPromise.paused){
                    playPromise.load();
                    playPromise.play();
                    audio_arr.splice(0, 1)
                }
            }         
        }            
            
        drawCtx.strokeRect(x, y, width, height);

    });
}

function play(file) {
    var audio = new Audio(file);

    audio.play();
  }
//Add file blob to a form and post
function postFile(file) {

    //Set options as form data
    let formdata = new FormData();
    formdata.append("image", file);
    formdata.append("threshold", scoreThreshold);
    
    formdata.append("class_name", className);

    let xhr = new XMLHttpRequest();
    xhr.open('POST', apiServer, true);
    xhr.onload = function () {
        if (this.status === 200) {
            let objects = JSON.parse(this.response);

            //draw the boxes
            drawBoxes(objects);

            //Save and send the next image
            imageCtx.drawImage(v, 0, 0, v.videoWidth, v.videoHeight, 0, 0, uploadWidth, uploadWidth * (v.videoHeight / v.videoWidth));
            // var start = new Date().getTime();
            imageCanvas.toBlob(postFile, 'image/jpeg');
            // var end = new Date().getTime();
            // console.log((end - start) / 1000 + "sec");
        }
        else {
            console.error(xhr);
        }
    };
    xhr.send(formdata);
}

//Start object detection
function startObjectDetection() {

    console.log("starting object detection");

    //Set canvas sizes base don input video
    drawCanvas.width = v.videoWidth;
    drawCanvas.height = v.videoHeight;

    imageCanvas.width = uploadWidth;
    imageCanvas.height = uploadWidth * (v.videoHeight / v.videoWidth);

    //Some styles for the drawcanvas
    drawCtx.lineWidth = 4;
    drawCtx.strokeStyle = "cyan";
    drawCtx.font = "20px Verdana";
    drawCtx.fillStyle = "cyan";

    //Save and send the first image
    imageCtx.drawImage(v, 0, 0, v.videoWidth, v.videoHeight, 0, 0, uploadWidth, uploadWidth * (v.videoHeight / v.videoWidth));
    imageCanvas.toBlob(postFile, 'image/jpeg');

}

//Starting events

//check if metadata is ready - we need the video size
v.onloadedmetadata = () => {
    console.log("video metadata ready");
    gotMetadata = true;
    if (isPlaying)
        startObjectDetection();
};

//see if the video has started playing
v.onplaying = () => {
    console.log("video playing");
    isPlaying = true;
    if (gotMetadata) {
        startObjectDetection();
    }
};

