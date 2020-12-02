<template>
  <div class="bg login-bg flex-center" style="overflow-y: auto; min-height: 621px;">
    <transition name="fade">
      <Loading v-if="isLoading"></Loading>
    </transition>
    <div class="main">
      <el-card class="box-card">
        <div slot="header" class="clearfix">
          <span>接口测试</span>
        </div>
        <el-form ref="form" :model="form" label-width="80px">
          <SelectList
            :data="{value: form.dev_id, set: componentsSet.dev_id}"
            v-on:resData="resSelectList">
          </SelectList>
          <el-form-item label="算法" prop="algorithm_id" :rules="[{ required: true, message: '请选择算法', trigger: 'blur' }]">
            <el-select v-model="form.algorithm_id" placeholder="请选择算法" class="w-100" filterable clearable @change="getAlgorithmSelected()">
              <el-option v-for="item in algorithmOptions"
                :label="item.algorithm_name"
                :key="item.id"
                :value="item.id"
                >
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="调用类型" prop="type_id" :rules="[{ required: true, message: '请选择调用类型', trigger: 'blur' }]">
            <el-select v-model="form.type_id" placeholder="请选择调用类型" class="w-100" filterable clearable @change="getTypeSelected(form.type_id)">
              <el-option v-for="item in typeOptions"
                :label="item.type_name"
                :key="item.type_id"
                :value="item.type_id"
                >
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="参数" prop="predict_classes" :rules="[{ required: predict_classes_require, message: '请输入参数', trigger: 'blur' }]">
            <el-input type="textarea" :autosize="{ minRows: 2, maxRows: 10}" v-model="form.predict_classes" placeholder='请输入参数，参数格式为json如{"key":"value"}'></el-input>
          </el-form-item>
          <el-form-item label="拍照" v-show="camera_show">
            <video id="video" width="340px" height="254px" autoplay="autoplay"></video>
            <canvas id="canvas" width="266px" height="198px" hidden="hidden"></canvas>
          </el-form-item>
          <el-form-item label="录音" v-show="audio_show">
            <div id="yysb_audio_waveform" class="form-control p-0 mb-3" style="border:1px solid rgb(222, 215, 215);"></div>
            <div class="btn-group" style="margin-top:10px">
              <el-button id="start" type="primary" @click="startRecording()" :disabled="startDis">开始</el-button>
              <el-button id="stop" type="primary" @click="stopRecording()" :disabled="stopDis">停止</el-button>
              <el-button id="play" type="primary" @click="playRecording()" :disabled="playDis">播放</el-button>
              <el-button @click="$router.back(-1)">取消</el-button>
            </div>
          </el-form-item>
          <UploadFile
            :data="{value: form.file_01, set: componentsSet.file_01}"
            v-on:resData="resUploadFile">
          </UploadFile>
          <UploadFile
            :data="{value: form.file_02, set: componentsSet.file_02}"
            v-on:resData="resUploadFile">
          </UploadFile>
          <el-form-item v-show="button_show">
            <el-button type="primary" @click="onSubmit('form',null)" v-if="form.type_id!=8">测试</el-button>
            <el-button type="primary" @click="captureSubmit()" v-if="form.type_id==8">拍照并识别</el-button>
            <el-button @click="$router.back(-1)">取消</el-button>
          </el-form-item>
          <el-form-item label="结果">
            <el-input type="textarea" :rows="5" v-model="result"></el-input>
          </el-form-item>
          <el-form-item label="图片" v-show="result_img_show">
            <img  name="result_img" :src="img_src">
          </el-form-item>
          <el-form-item label="音频" v-show="result_audio_show">
            <div id="yyhc_result_waveform" class="form-control p-0 mb-3"></div>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script>
import SelectList from '@/components/SelectList.vue';
import UploadFile from '@/components/UploadFile.vue';
import Loading from '@/components/Loading.vue'
import $ from 'jquery'
import WaveSurfer from 'wavesurfer.js';
import Microphone from 'wavesurfer.js/dist/plugin/wavesurfer.microphone.js'
import Recorder from 'recorderjs';
//import Recorder from '@/plugins/recorder.js';

export default {
  name: 'ApiTest',
  components: {
    SelectList,
    UploadFile,
    Loading
  },
  data (){
    return {
      predict_classes_require: false,
      camera_show: false,
      audio_show: false,
      mediaStreamTrack: null,
      audio_context: null,
      recorder: null,
      button_show: true,
      recording_wavesurfer: null,
      startDis: false,
      stopDis: true,
      playDis: true,
      result_img_show: false,
      result_audio_show: false,
      img_src: require('@/assets/image-bg.png'),
      form: {
        dev_id: null,
        algorithm_id: null,
        type_id: null,
        predict_classes: '',
        file_01: [],
        file_02: []
      },
      isLoading: false,
      result: null,
      algorithmOptions: [],
      typeOptions:[{type_id:1, type_name:'纯参数调用'},{type_id:2, type_name:'图片处理'},{type_id:3, type_name:'图片对比'},{type_id:4, type_name:'文本处理'},{type_id:5, type_name:'语音处理'},{type_id:6, type_name:'文本对比'},{type_id:7, type_name:'视频处理'},{type_id:8, type_name:'摄像头'},{type_id:9, type_name:'麦克风'}],
      componentsSet: {
        dev_id: {
          name: 'dev_id',
          label: '设备',
          apiUrl: '/API/base-api/query-online-dev/',
          optionLabel: 'dev_name',
          addBtn: false,
          deleteBtn: false
        },
        // algorithm_id: {
        //   name: 'algorithm_id',
        //   label: '算法',
        //   apiUrl: '/API/base-api/api-algorithm/',
        //   optionLabel: 'algorithm_name',
        //   addBtn: false,
        //   deleteBtn: false
        // },
        // algorithm_type_id: {
        //   name: 'type_id',
        //   label: '算法类型',
        //   apiUrl: '/API/base-api/algorithm-model/',
        //   optionLabel: 'type_name',
        //   addBtn: false,
        //   deleteBtn: false
        // },
        devServer: null,
        file_01: {
          name: 'file_01',
          label: '文件1',
          required: false,
          show: false
        },
        file_02: {
          name: 'file_02',
          label: '文件2',
          required: false,
          show: false
        }
      }
    }
  },
  methods: {
    //select组件赋值
    resSelectList(res) {
      this.form[res.set.name] = res.value;
      this.$refs['form'].clearValidate([res.set.name]);
      this.result = '';
      this.result_img_show = false;
      this.result_audio_show = false;
      this.form.predict_classes='';
      this.result = '';
      this.result_img_show = false;
      this.result_audio_show = false;
      this.loadAlgorithm(res.value);
    },
    //上传组件赋值
    resUploadFile(res) {
      this.form[res.set.name] = res.value;
      this.$refs['form'].clearValidate([res.set.name]);
    },
    loadAlgorithm(devId) {
      axios.get('/API/base-api/dev-management/'+devId+'/').then( res => {
          let _this = this;
          _this.devServer = res.data.ip;
          if(_this.devServer.indexOf('127.0.0.1')!=-1||_this.devServer.indexOf('localhost')!=-1){
            _this.devServer = '';
          }else{
            _this.devServer = "http://"+_this.devServer;
          }
          //查询算法
          axios({
            url: _this.devServer+'/API/base-api/api-algorithm/',
            method: 'get',
            // withCredentials: true
          }).then(function (response) {
            _this.algorithmOptions = response.data.results;
          })
      })
    },
    getAlgorithmSelected() {
      let _this = this;
      _this.form.predict_classes='';
      _this.result = '';
      _this.result_img_show = false;
      _this.result_audio_show = false;
    },
    openCamera() {
      let _this = this;
      try {
        //初始化
        window.AudioContext = window.AudioContext || window.webkitAudioContext;
        navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia;
        window.URL = window.URL || window.webkitURL;
      } catch (e) {
          _this.$message({
            type: 'info',
            message: '该浏览器不支持调用web资源'
          });
      }
      let constraints = {
          video: {facingMode: 'user', width: 340, height: 254},
          audio: false
      };
      navigator.mediaDevices.getUserMedia(constraints).then((stream) => {
          _this.mediaStreamTrack = stream.getTracks()[0];
          let video = document.getElementById("video");
          video.srcObject = stream;
          video.play();
      }).catch(error);

      function error(error){
          if(error.name.indexOf('NotReadableError')!=-1){
              navigator.mediaDevices.getUserMedia(constraints).then((stream) => {
                _this.mediaStreamTrack = stream.getTracks()[0];
                let video = document.getElementById("video");
                video.srcObject = stream;
                video.play();
              }).catch(error);
          }
      }
    },
    openAudio() {
      let _this = this;
      _this.audio_context = new AudioContext;
      navigator.mediaDevices.getUserMedia({audio:true}).then((stream) => {
           _this.mediaStreamTrack = stream.getTracks()[0];
           var input = _this.audio_context.createMediaStreamSource(stream);
           _this.recorder = new Recorder(input);
      }).catch(audio_error);

      function audio_error(error){
          if(error.name.indexOf('NotReadableError')!=-1){
              navigator.mediaDevices.getUserMedia({audio:true}).then((stream) => {
                _this.mediaStreamTrack = stream.getTracks()[0];
                var input = _this.audio_context.createMediaStreamSource(stream);
                _this.recorder = new Recorder(input);
            }).catch(audio_error);
          }
      }

      if(_this.recording_wavesurfer==null){
        var waveform = document.getElementById("yysb_audio_waveform");
        //判断是否包含子元素
        if (waveform.hasChildNodes()) {
          var len = waveform.childNodes.length;     //子元素的个数
          for (var i = 0; i < len; i++) {     //遍历
            waveform.removeChild(waveform.childNodes[0]);//从第一个元素开始删除
          }
        }
        //创建录音
        _this.recording_wavesurfer = WaveSurfer.create({
          container     : '#yysb_audio_waveform',
          waveColor     : 'black',
          interact      : false,
          cursorWidth   : 0,
          plugins: [
            Microphone.create()
          ]
        })
      }
    },
    closeMedia() {
      let _this = this;
      _this.mediaStreamTrack && _this.mediaStreamTrack.stop();
    },
    startRecording() {
      let _this = this;
      _this.startDis = true;
      _this.stopDis = false;
      _this.playDis = false;
      _this.recording_wavesurfer.microphone.start();
      _this.recorder && _this.recorder.record();
    },
    stopRecording() {
      let _this = this;
      _this.startDis = false;
      _this.stopDis = true;
      _this.playDis = false;
      _this.recording_wavesurfer.microphone.stop();
      _this.recorder && _this.recorder.stop();
      _this.createDownloadLink();
      _this.recorder.clear();
    },
    createDownloadLink() {
      let _this = this;
      _this.recorder && _this.recorder.exportWAV(function(blob) {
        let url = URL.createObjectURL(blob);
        _this.recording_wavesurfer.load(url);
        _this.onSubmit('form', blob);
      })
    },
    playRecording() {
      let _this = this;
      _this.recording_wavesurfer.on('ready', function () {
        _this.recording_wavesurfer.play();
      });
    },
    getTypeSelected(val) {
        let _this = this;
        _this.form.predict_classes='';
        if(val==1){
            _this.predict_classes_require=true;
            _this.componentsSet.file_01.show=false;
            _this.componentsSet.file_01.required=false;
            _this.componentsSet.file_02.show=false;
            _this.componentsSet.file_02.required=false;
            _this.camera_show = false;
            _this.closeMedia();
            _this.audio_show = false;
            _this.recording_wavesurfer = null;
            _this.button_show = true;
        }else if(val==2){
            _this.predict_classes_require=false;
            _this.componentsSet.file_01.show=true;
            _this.componentsSet.file_01.label="图片";
            _this.componentsSet.file_01.accept='.png,.jpg';
            _this.componentsSet.file_01.required=true;
            _this.componentsSet.file_02.show=false;
            _this.componentsSet.file_02.required=false;
            _this.camera_show = false;
            _this.closeMedia();
            _this.audio_show = false;
            _this.recording_wavesurfer = null;
            _this.button_show = true;
        }else if(val==3){
            _this.predict_classes_require=false;
            _this.componentsSet.file_01.label="图片1";
            _this.componentsSet.file_01.accept='.png,.jpg';
            _this.componentsSet.file_01.show=true;
            _this.componentsSet.file_01.required=true;
            _this.componentsSet.file_02.label="图片2";
            _this.componentsSet.file_02.accept='.png,.jpg';
            _this.componentsSet.file_02.show=true;
            _this.componentsSet.file_02.required=true;
            _this.camera_show = false;
            _this.closeMedia();
            _this.audio_show = false;
            _this.recording_wavesurfer = null;
            _this.button_show = true;
        }else if(val==4){
            _this.predict_classes_require=false;
            _this.componentsSet.file_01.label="文本";
            _this.componentsSet.file_01.accept='.txt';
            _this.componentsSet.file_01.show=true;
            _this.componentsSet.file_01.required=true;
            _this.componentsSet.file_02.show=false;
            _this.componentsSet.file_02.required=false;
            _this.camera_show = false;
            _this.closeMedia();
            _this.audio_show = false;
            _this.recording_wavesurfer = null;
            _this.button_show = true;
        }else if(val==5){
            _this.predict_classes_require=false;
            _this.componentsSet.file_01.label="音频文件";
            _this.componentsSet.file_01.accept='.wav';
            _this.componentsSet.file_01.show=true;
            _this.componentsSet.file_01.required=true;
            _this.componentsSet.file_02.show=false;
            _this.componentsSet.file_02.required=false;
            _this.camera_show = false;
            _this.closeMedia();
            _this.audio_show = false;
            _this.recording_wavesurfer = null;
            _this.button_show = true;
        }else if(val==6){
            _this.predict_classes_require=false;
            _this.componentsSet.file_01.label="文本1";
            _this.componentsSet.file_01.accept='.txt';
            _this.componentsSet.file_01.show=true;
            _this.componentsSet.file_01.required=true;
            _this.componentsSet.file_02.label="文本2";
            _this.componentsSet.file_02.accept='.txt';
            _this.componentsSet.file_02.show=true;
            _this.componentsSet.file_02.required=true;
            _this.camera_show = false;
            _this.closeMedia();
            _this.audio_show = false;
            _this.recording_wavesurfer = null;
            _this.button_show = true;
        }else if(val==7){
            _this.predict_classes_require=false;
            _this.componentsSet.file_01.label="视频文件";
            _this.componentsSet.file_01.accept='.webm,.mp4';
            _this.componentsSet.file_01.show=true;
            _this.componentsSet.file_01.required=true;
            _this.componentsSet.file_02.show=false;
            _this.componentsSet.file_02.required=false;
            _this.camera_show = false;
            _this.closeMedia();
            _this.audio_show = false;
            _this.recording_wavesurfer = null;
            _this.button_show = true;
        }else if(val==8){
          _this.predict_classes_require=false;
          _this.componentsSet.file_01.show=false;
          _this.componentsSet.file_01.required=false;
          _this.componentsSet.file_02.show=false;
          _this.componentsSet.file_02.required=false;
          _this.camera_show = true;
          _this.closeMedia();
          _this.openCamera();
          _this.audio_show = false;
          _this.recording_wavesurfer = null;
          _this.button_show = true;
        }else if(val==9){
          _this.predict_classes_require=false;
          _this.componentsSet.file_01.show=false;
          _this.componentsSet.file_01.required=false;
          _this.componentsSet.file_02.show=false;
          _this.componentsSet.file_02.required=false;
          _this.camera_show = false;
          _this.audio_show = true;
          _this.recording_wavesurfer = null;
          _this.button_show = false;
          _this.closeMedia();
          _this.openAudio();
        }
        _this.result = '';
        _this.result_img_show = false;
        _this.result_audio_show = false;
    },
    isJSON(str) {
      if (typeof str == 'string') {
          try {
              var obj=JSON.parse(str);
              if(typeof obj == 'object' && obj ){
                  return true;
              }else{
                  return false;
              }
          } catch(e) {
              return false;
          }
      }
    },
    onSubmit(formName, blob) {
      let _this = this;
      _this.$refs[formName].validate((valid) => {
        if (valid) {
            var predictBoolean = true;
            if(_this.form.predict_classes!=null&&_this.form.predict_classes!=''){
              if(!_this.isJSON(_this.form.predict_classes)){
                predictBoolean = false;
                _this.$message({
                  type: 'info',
                  message: '参数必须为json格式的字符串'
                });
              }
            }
            //数据
            if(predictBoolean){
              let fd = new FormData();
              if(_this.form.type_id==8&&blob!=null){
                fd.append('file1_name', blob, 'capture')
              }else if(_this.form.type_id==9&&blob!=null){
                fd.append('file1_name', blob, 'audio.wav')
              }else{
                if(_this.form.file_01.length){ fd.append('file1_name', _this.form.file_01[0].raw, _this.form.file_01[0].name) }
              }
              if(_this.form.file_02.length){ fd.append('file2_name', _this.form.file_02[0].raw, _this.form.file_02[0].name) }
              fd.append('algorithm_id', _this.form.algorithm_id);
              fd.append('type_id', _this.form.type_id);
              fd.append('predict_classes', _this.form.predict_classes);
              _this.$message({
                  type: 'info',
                  message: '正在调用接口，请稍候！'
              });
              // 接口
              const userData = JSON.parse(sessionStorage.getItem('user'));
              let userId = userData.id;
              axios({
                url: '/API/sys-parameters-manage/?userId='+userId,
                method: 'get',
                // withCredentials: true
              }).then(function (response) {
                fd.append('zhiyun_id', response.data.result_data.zhiyun_id);
                fd.append('zhiyun_key', response.data.result_data.zhiyun_key);
                fd.append('zhiyun_server', response.data.result_data.zhiyun_server);
                fd.append('sensor_a_mac', response.data.result_data.sensor_a_mac);
                fd.append('sensor_b_mac', response.data.result_data.sensor_b_mac);
                fd.append('sensor_c_mac', response.data.result_data.sensor_c_mac);
                fd.append('sensor_d_mac', response.data.result_data.sensor_d_mac);
                fd.append('sensor_eh_mac', response.data.result_data.sensor_eh_mac);
                fd.append('sensor_el_mac', response.data.result_data.sensor_el_mac);
                fd.append('baidu_app_id', response.data.result_data.baidu_app_id);
                fd.append('baidu_app_key', response.data.result_data.baidu_app_key);
                fd.append('baidu_secret_key', response.data.result_data.baidu_secret_key);
                fd.append('baidu_service_id', response.data.result_data.baidu_service_id);
                fd.append('tencent_secret_id', response.data.result_data.tencent_secret_id);
                fd.append('tencent_secret_key', response.data.result_data.tencent_secret_key);
                fd.append('face_api_key', response.data.result_data.face_api_key);
                fd.append('face_api_secret', response.data.result_data.face_api_secret);
                fd.append('xfyun_api_key', response.data.result_data.xfyun_api_key);
                fd.append('xfyun_api_secret', response.data.result_data.xfyun_api_secret);
                _this.isLoading = false;
                axios({
                  url: _this.devServer+'/API/algorithms/',
                  data: fd,
                  method: 'post'
                }).then( res => {
                  _this.result = JSON.stringify(res.data, null, 4);
                  if(res.data.code==200){
                      if(res.data.hasOwnProperty("image")){
                      _this.result_img_show = true;
                      _this.img_src = 'data:image/jpeg;base64,' + res.data.image;
                    }else if(res.data.hasOwnProperty("audio")){
                        _this.result_audio_show = true;
                        var wavesurfer = WaveSurfer.create({
                            container: '#yyhc_result_waveform',
                            waveColor: 'black',
                            progressColor: 'purple'
                        });
                        wavesurfer.load(res.data.audio);
                        wavesurfer.on('ready', function () {
                          wavesurfer.play();
                        });
                    }
                  }else if(res.data.code==300){
                      _this.$message({
                        type: 'error',
                        message: res.data.message,
                      });
                  }else{
                      _this.$message({
                        type: 'error',
                        message: '处理异常，请重试！'
                      });
                  }
                  _this.isLoading = false;
                })
              })
            }
        } else {
          return false;
        }
      });
    },
    isJsonFormat(str) {
        try {
            $.parseJSON(str);
        } catch (e) {
            return false;
        }
        return true;
    },
    dataURItoBlob(base64Data){
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
    },
    captureSubmit() {
      var _this = this;
      let video = document.getElementById("video");
      let canvas = document.getElementById("canvas");
      let ctx = canvas.getContext('2d');
      ctx.drawImage(video, 0, 0, 266, 198);
      let imgBase64 = canvas.toDataURL("image/jpeg", 1.0);
      var blob = _this.dataURItoBlob(imgBase64);
      _this.onSubmit('form',blob);
    }
  }
}
</script>

<style scoped lang="scss">
  .main{
    box-sizing: border-box;
    overflow-y: auto;
    padding: 1rem 0;
    max-height: 100%;
    width: 100%;
  }
  .box-card{
    width: 60%;
    margin: 0 auto;
  }
</style>
