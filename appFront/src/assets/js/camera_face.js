export const camera_face = function (){
  //初始化
  var settingParm = {
    video: null,
    canvas: null,
    captureCanvas: null,
    videoWidth: 640,
    videoHeight: 480,
    hw: 480/640,

    login: false,
    loginUrl: null
  }

  var publicParm = {
    loginStatus: true,
    rect: null
  }

  var self = this;

  //extend
  self.extend = function () {
    var length = arguments.length;
    var target = arguments[0] || {};
    if (typeof target!="object" && typeof target != "function") {
        target = {};
    }
    if (length == 1) {
        target = this;
        i--;
    }
    for (var i = 1; i < length; i++) { 
        var source = arguments[i]; 
        for (var key in source) { 
            // 使用for in会遍历数组所有的可枚举属性，包括原型。
            if (Object.prototype.hasOwnProperty.call(source, key)) { 
                target[key] = source[key]; 
            } 
        } 
    }
    return target; 
  };

  //创建Html
  self.createHtml = function (settings){

    self.extend(settingParm,settings);

    var object = document.querySelector('[data-type="cameraFace"]');
    object.style.position = 'relative';
    object.style.width = '100%';
    var html = '<video id="video" preload autoplay loop muted style="position:relative;width:100%;"></video>' +
              '<canvas id="canvas" style="position:absolute;top:0;left:0;"></canvas>'+
              '<canvas id="captureCanvas" width="100" height="100" style="display:none;"></canvas>';
    object.innerHTML = html;

    settingParm.video = document.getElementById('video');
    settingParm.canvas = document.getElementById('canvas');
    settingParm.captureCanvas = document.getElementById('captureCanvas');

    self.openCamera();
  };

  //打开摄像头
  self.openCamera = function (){
    var canvas = settingParm.canvas;
    var video = settingParm.video;

    canvas.width = canvas.parentNode.clientWidth;
    canvas.height = canvas.parentNode.clientWidth*settingParm.hw;

    video.width = canvas.parentNode.clientWidth;
    video.height = canvas.parentNode.clientWidth*settingParm.hw;

    var context = canvas.getContext('2d');
    var tracker = new tracking.ObjectTracker('face');
    tracker.setInitialScale(5);
    tracker.setStepSize(2);
    tracker.setEdgesDensity(0.1);
    tracking.track('#video', tracker, { camera: true });
    tracker.on('track', function(event) {
      context.clearRect(0, 0, canvas.width, canvas.height);
      if (event.data.length === 0) {
        publicParm.rect = null;
      } else {
        event.data.forEach(function(rect) {
          publicParm.rect = rect;
          context.strokeStyle = '#006281';
          context.strokeRect(rect.x, rect.y, rect.width, rect.height);
          // context.font = '11px Helvetica';
          // context.fillStyle = "#fff";
          // context.fillText('x: ' + rect.x + 'px', rect.x + rect.width + 5, rect.y + 11);
          // context.fillText('y: ' + rect.y + 'px', rect.x + rect.width + 5, rect.y + 22);
          //登录触发
          if(settingParm.login){
            if (publicParm.loginStatus) {
              publicParm.loginStatus = false;
              self.login()
            }
          }
        });
      }
    });
  };

  //截图
  self.capture = function (type){

    var video = settingParm.video;
    var canvas = settingParm.captureCanvas;
    var context = canvas.getContext('2d');
    var rect = publicParm.rect;

    //video缩放比例
    var prox = video.videoWidth/video.width;
    var proy = video.videoHeight/video.height;
    if (rect) {
      //预览截图
      context.drawImage(video, rect.x*prox, rect.y*proy, rect.width*prox, rect.height*proy, 0, 0, canvas.width, canvas.height); 

      //截图封装blob对象
      var base64Data = canvas.toDataURL("image/jpeg", 1.0);
      var blob = self.dataURItoBlob(base64Data);

      if (type) {
        return blob
      }else{
        return base64Data
      }
    }else{
      publicParm.rect = null;
      return false
    }
  };

  //封装blob对象
  self.dataURItoBlob = function (base64Data){
    var byteString;
    if (base64Data.split(',')[0].indexOf('base64') >= 0)
      byteString = atob(base64Data.split(',')[1]);
    else
      byteString = unescape(base64Data.split(',')[1]);
    var mimeString = base64Data.split(',')[0].split(':')[1].split(';')[0];
    var ia = new Uint8Array(byteString.length);
    for (var i = 0; i < byteString.length; i++) {
      ia[i] = byteString.charCodeAt(i);
    }
    return new Blob([ia], {type: mimeString});
  };

  //登录
  self.login = function (){
    var blob = self.capture(true);//false返回base64，true返回blob封装。

    //组装formdata
    var fd = new FormData(document.forms[0]);
    fd.append("headImg", blob, 'image.png');

    //上传
    axios.post(settingParm.loginUrl, fd).then(function (response) {
      if(response.data.code == 1001){
        this.$message({
          message: '登录成功！2秒后自动跳转至首页。',
          type: 'success',
          duration: 2000,
          onClose: () => {
            this.$router.push({path:'/'})
          }
        })
      }else if(response.data.code == 1009){
        this.$message({
          message: '未注册的用户。',
          type: 'error',
          duration: 2000
        })
      }
      console.log(response);
    }).catch(function (error) {
      console.log(error);
      setTimeout(function(){
        publicParm.loginStatus = true;
      },2000)
    })
  }

}