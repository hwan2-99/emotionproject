//webkitURL is deprecated but nevertheless

URL = window.URL || window.webkitURL;

var gumStream; 						//stream from getUserMedia()
var rec; 							//Recorder.js object
var input; 							//MediaStreamAudioSourceNode we'll be recording

var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record

var public_key;
var symmetrical_key;
var encryption_algorithm; // encryption_algorithm : number

function setEncryptionAlgorithm(algorithm){
	encryption_algorithm = algorithm;
}

function setSymmetricalKey(key){
	symmetrical_key = key;
}

function setPublicKey(key){
	public_key = key;
}

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

async function createDownloadLink(blob) {
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
	var fd = new FormData();
	console.log("목소리")

	//blob.arrayBuffer()
	//await new Response(blob).text()
	let reader = new FileReader();
	reader.onload = async function(){
		// 암호화 대상 메시지
		var plainText = reader.result.split(',')[1]; // base64 인코딩
		// 대칭키 발급
		if(encryption_algorithm == 1){
			var key_string = symmetrical_key;
		}else if(encryption_algorithm == 2){
			var key_string = Math.random().toString(36).substring(2, 12) + new Date().getTime().toString(36).substring(2);
		}else{
			throw new Error('encryption_algorithm is required');
		}
		// 대칭 암호화 - JS ENCRYPTION ECB
		key = CryptoJS.enc.Utf8.parse(key_string); // 대칭 키
		var encrypted = CryptoJS.AES.encrypt(plainText, key, {mode: CryptoJS.mode.ECB});
		encrypted = encrypted.toString();

		if(encryption_algorithm == 1){
			// nothing to do...
		}else if(encryption_algorithm == 2){
			// 비대칭 암호화
			var crypt = new JSEncrypt();
			crypt.setPrivateKey(public_key);// 비대칭 키 설정
			// 암호화
			var encrypted_key = crypt.encrypt(key_string);
			fd.append("encrypted_key",encrypted_key);
		}else{
			throw new Error('encryption_algorithm is required');
		}

		//fd.append("audio_data", blob, filename);
		fd.append("encrypted_audio_data",encrypted)
		fd.append("startTime", new Date().getTime());
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
	await reader.readAsDataURL(blob);
}