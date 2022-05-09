//webkitURL is deprecated but nevertheless

URL = window.URL || window.webkitURL;

var gumStream; 						//stream from getUserMedia()
var rec; 							//Recorder.js object
var input; 							//MediaStreamAudioSourceNode we'll be recording

var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record

function startRecording() {
	console.log("recordButton clicked");

	document.getElementById("voice_loading").style.display = "block";
    var constraints = { audio: true, video:false }


	navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
		console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

		audioContext = new AudioContext();

		document.getElementById("formats").innerHTML="Format: 1 channel pcm @ "+audioContext.sampleRate/1000+"kHz"

		gumStream = stream;

		input = audioContext.createMediaStreamSource(stream);

		rec = new Recorder(input,{numChannels:1})

		rec.record()

		console.log("Recording started");

	}).catch(function(err) {
	});
}

function stopRecording() {
	console.log("stopButton clicked");

	//tell the recorder to stop the recording
	rec.stop();

	//stop microphone access
	gumStream.getAudioTracks()[0].stop();

	//create the wav blob and pass it on to createDownloadLink
	rec.exportWAV(createDownloadLink);
}

function createDownloadLink(blob) {
	console.log()
	var url = URL.createObjectURL(blob);
	var au = document.createElement('audio');
	var li = document.createElement('li');
	var link = document.createElement('a');

	//name of .wav file to use during upload and download (without extendion)
	var filename = "test";

	//add controls to the <audio> element
	au.controls = true;
	au.src = url;

	//upload link
	var upload = document.createElement('a');
	upload.href="#";
	upload.innerHTML = "Upload";
	var xhr=new XMLHttpRequest();
	var fd=new FormData();
	console.log("목소리")
	fd.append("audio_data", blob, filename);

	$.ajax({
			headers: {'X-CSRFToken': csrftoken},
            type : 'POST',
            url : '/v2/voice',
            data : fd,
            dataType: 'json',
            processData: false,    // 반드시 작성
            contentType: false,    // 반드시 작성
            success : function(result){
                if(result.data.negative > 0.4) {
                    alert("이상 징후가 감지되었습니다. 추가인증을 해주세요..")
                    window.location.href = '/v2/fail';
                }
            },
            error : function(xtr,status,error){-
               alert("측정 오류. 기존 페이지를 유지합니다.")
            }
        });

	document.getElementById("voice_loading").style.display = 'none';
}
