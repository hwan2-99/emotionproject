## 개발환경


- django
- mysql
- mongodb
- Html/css/javascript

## 초기 설정

#### my_settings.py 설정 (manage.py와 같은 위치)
```
SECRET_KEY = {
    '비밀번호 키(개발자에게 요청)'
}

EMAIL = {
    'EMAIL_BACKEND' : 'django.core.mail.backends.smtp.EmailBackend',
    'EMAIL_USE_TLS' : True,
    'EMAIL_PORT' : 587,
    'EMAIL_HOST' : 'smtp.gmail.com',
    'EMAIL_HOST_USER' : '보내는 사람의 이메일',
    'EMAIL_HOST_PASSWORD' : '이메일 비밀번호 (개발자에게 요청)',
    'REDIRECT_PAGE' : 'https://192.168.64.94:8000/v2/main'
}

ALLOWED_HOSTS = ['*', '127.0.0.1', '192.168.64.94', '192.168.64.118']
```

## 설치


모듈 설치

<aside>
💡 `pip install -r requirements.txt`

</aside>

migration 설정

```
# 마이그레이션 파일 생성$ python manage.py makemigrations <app-name>

# 마이그레이션 적용$ python manage.py migrate <app-name>

# 마이그레이션 적용 현황$ python manage.py showmigrations <app-name>

# 지정 마이그레이션의 SQL 내역
 python manage.py sqlmigrate <app-name> <migration-name>
```

## 실행


<aside>
💡 `python manage.py runsslserver 192.168.64.118:8000`

</aside>

## 주요 파일 설명

### emotionProject

- 전반적인 환경 관리

### emotionSys

- MVC로 처리할 API 통신할 메서드 관리

### faceEmotion

- 얼굴 감정 인식 및 얼굴 유사도 인식
- emotion_model.hdf5 모델을 이용하여 얼굴 감정 인식
- [face.py](http://face.py) 는 감정인식 모듈
- face_Recognition.py 는 얼굴 유사도 모듈

### restApi

- REST API 통신이 필요한 메서드 관리
- voice method
    - 음성 데이터를 받아 음성 모델에 결과 값을 전달
- face method
    - 이미지 값과 측정 값을 받아서

### static

- 정적 데이터 관리
- ex) css, js, image

### template

- html 관리
- face

```jsx

        const video = document.getElementById("video");

        // face api 허용
        Promise.all([
          faceapi.nets.tinyFaceDetector.loadFromUri("{% static 'assets/models' %}"),
          faceapi.nets.faceLandmark68Net.loadFromUri("{% static 'assets/models' %}"),
          faceapi.nets.faceRecognitionNet.loadFromUri("{% static 'assets/models' %}"),
          faceapi.nets.faceExpressionNet.loadFromUri("{% static 'assets/models' %}"),
        ]).then(startVideo);

        // 비디오 시작 함수
        function startVideo() {
          navigator.mediaDevices
            .getUserMedia({ video: true })
            .then(function (stream) {
              video.srcObject = stream;
            })
            .catch(function (err) {
              console.log(err);
            });
        }

        // 비디오 사이즈
        video.addEventListener("playing", () => {
          const canvas = faceapi.createCanvasFromMedia(video);
          document.body.append(canvas);
          const displaySize = { width: video.width, height: video.height };
          faceapi.matchDimensions(canvas, displaySize);

        });
        // 비동기 처리 얼굴 표정 값
        setInterval(async () => {
            document.getElementById("face_loading").style.display = 'block';
            const detections = await faceapi
              .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
              .withFaceLandmarks()
              .withFaceExpressions();
            var data = detections[0].expressions.fearful;
            console.log(parseFloat(data).toFixed(8));

            const canvas = document.getElementById("canvas_video");
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext("2d").drawImage(video, 0, 0,canvas.width, canvas.height);
            const dataURL = canvas.toDataURL();
            var fd=new FormData();
            fd.append("faceURL", dataURL)
            fd.append("neutral", parseFloat(detections[0].expressions.neutral).toFixed(8));
            fd.append("happy", parseFloat(detections[0].expressions.happy).toFixed(8));
            fd.append("angry", parseFloat(detections[0].expressions.angry).toFixed(8));
            fd.append("sad", parseFloat(detections[0].expressions.sad).toFixed(8));
            fd.append("fearful", parseFloat(detections[0].expressions.fearful).toFixed(8));
            $.ajax({
                headers: {'X-CSRFToken': csrftoken},
                type : 'POST',
                url : '/v2/face',
                data : fd,
                dataType: 'json',
                processData: false,    // 반드시 작성
                contentType: false,    // 반드시 작성
                success : function(result){
                    fear = parseFloat(detections[0].expressions.fearful).toFixed(8)
                    if(fear > 0.15 || result.face == 'X') {``
                        alert("이상 징후가 감지되었습니다. 추가인증을 해주세요.")
                        window.location.href = '/v2/fail';
                    }

                },
                error : function(xtr,status,error){
                   alert("측정 오류. 기존 페이지를 유지합니다.")
                }
            });

          }, 10000);
        document.getElementById("face_loading").style.display = 'none';
        //미디어 허용
        if (navigator.mediaDevices.getUserMedia) {
          navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
              video.srcObject = stream;
            })
            .catch(function (err0r) {
              console.log("Something went wrong!");
            });
        }
```

- 모델 적용이 완료되면 캠이 켜지며 10초 반복으로 캠을 캡쳐하여 이미지에 대한 감정과 서버에 전송 하여 유사도 값을 받은 후 결과 처리
- csrf 처리

```jsx

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie &&document.cookie !== '') {
        const cookies =document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
constcsrftoken= getCookie('csrftoken');
```

- voice

```jsx
detectTF = true;
setInterval(function () {
    startRecording();
    setTimeout(stopRecording, 5000);
}, 10000);

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
```

- 목소리를 5초간 녹음을 해서 데이터를 서버에 전송
- 10초로 계속 반복

### voiceEmotion

- 음성 감정 인식 모듈
