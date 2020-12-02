var audio_context;
var recorder;
var maxTime = 60;
var timer = null;
var count = 0;
window.onload = function init() {
    try {
        //初始化
        window.AudioContext = window.AudioContext || window.webkitAudioContext;
        navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia;
        window.URL = window.URL || window.webkitURL;
    } catch (e) {
        console.log(e);
        swal({
            icon: "error",
            title: "不支持",
            text: "该浏览器不支持调用web资源！",
            timer: 2000,
            button: false
        });
    }
    //打开摄像头和麦克风
    getMedia()
};

//打开摄像头
function getMedia() {
    //调用麦克风
    navigator.mediaDevices.getUserMedia({
        audio: true
    }).then((stream) => {
        audio_context = new AudioContext;
        var input = audio_context.createMediaStreamSource(stream);
        recorder = new Recorder(input);
    }).catch(audio_error);

    function audio_error(error) {
        if (error.name.indexOf('NotReadableError') != -1) {
            navigator.mediaDevices.getUserMedia({
                audio: true
            }).then((stream) => {
                audio_context = new AudioContext;
                var input = audio_context.createMediaStreamSource(stream);
                recorder = new Recorder(input);
            }).catch(audio_error);
        }
    }

}

//获取cookie值
function getCookie(name) {
    var value = '; ' + document.cookie
    var parts = value.split('; ' + name + '=')
    if (parts.length === 2) {
        return parts.pop().split(';').shift()
    }
}


//开始录音
function startRecording() {
    $('.CHAT3').css('display', '')
    $('.CHAT2').css('display', 'none')
    timer = setInterval(() => {
        $('.maxtime').html(--maxTime + 's');
        if (maxTime == 0) {
            stopRecording()
        }
    }, 1000);

    recorder && recorder.record();
}

//结束录音
function stopRecording() {
    if (timer) {
        maxTime = 60
        $('.maxtime').html('60s');
        clearInterval(timer)
    }
    $('.CHAT2').css('display', '')
    $('.CHAT3').css('display', 'none')

    recorder && recorder.stop();
    createDownloadLink();
    recorder.clear();
}

function createDownloadLink() {
    recorder && recorder.exportWAV(function (blob) {
        userData = JSON.parse(sessionStorage.getItem("user"));
        patient_id = sessionStorage.getItem("patient_id")
        let formData = new FormData();
        formData.set('file1_name', blob, 'audio.wav');
        formData.append('user_id', userData.id);
        formData.append('patient_id', patient_id);
        $.ajax({
            url: '/API/voice-recognition/',
            method: 'POST',
            processData: false, // 必须
            contentType: false, // 必须
            dataType: 'json',
            data: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success(result) {
                if (result.code == 200) {
                    count+=1
                    console.log(result);
                    //结束录音，请求后台转换为文字，拿到文字，放入对话框中
                    if (count %2 == 0){
                        var voice_text = result.msg;
                        var uuid = 'chat' + guid();
                        appendHistory(1, voice_text, uuid);
                    }else{
                        var voice_text = result.msg;
                        var uuid = 'chat' + guid();
                        appendHistory(0, voice_text, uuid);
                    }
                    
                } else {
                    swal({
                        title: "识别失败！",
                        icon: "error",
                        text: "2秒后自动关闭。",
                        timer: 2000,
                        button: false
                    })
                }
            },
            error(error) {
                console.log(error);
                swal('数据异常', {
                    icon: "error",
                    button: false,
                    timer: 2000,
                });
            }
        })
    })
}

function appendHistory(type, query, uuid) {
    if (!uuid) return;
    if (type == 0) {
        // 用户消息
        $('.history').append(`
              <div class="right">
                 <div class="bubble bubble-green">
                   <div class="bubble-avatar"><i class="fas fa-user"></i></div>
                   <p style="text-align: left" id="${uuid}">${query}</p>
                 </div>
              </div>
`);
    } else {
        $('.history').append(`
              <div class="left">
                 <div class="bubble bubble-white">
                   <div class="bubble-avatar"><image src="./static/robot.png" width=32px attr="robot" /></div>
                   <p style="text-align: left" id="${uuid}">${query}</p>
                 </div>
              </div>
`);
    }
    $("#" + uuid).fadeIn(2000);
    var scrollHeight = $('.history').prop("scrollHeight");
    $('.history').scrollTop(scrollHeight, 200);
}


//用于生成uuid
function S4() {
    return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
}

function guid() {
    return (S4() + S4() + "-" + S4() + "-" + S4() + "-" + S4() + "-" + S4() + S4() + S4());
}
