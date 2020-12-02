<template>
  <el-container>
    <el-header>
      <el-row>
        <el-col :span="3" style="float:right;line-height: 56px;">
          <div class="grid-content bg-purple">
            <el-select v-model="value" filterable placeholder="请选择病人" @change="change">
              <el-option
                v-for="item in patientArray"
                :key="item.id"
                :label="item.patient_name"
                :value="item.id"
              ></el-option>
            </el-select>
          </div>
        </el-col>
        <el-col :span="21">
          <div class="grid-content">
            <!-- <el-button type="primary" icon="el-icon-plus">添加病人信息</el-button> -->
            <ul>
              <el-col :span="6">
                <li>
                  <span>姓名：</span>
                  <label for>{{currentName}}</label>
                </li>
              </el-col>
              <el-col :span="6">
                <li>
                  <span>性别：</span>
                  <label for>{{currentSex}}</label>
                </li>
              </el-col>
              <el-col :span="6">
                <li>
                  <span>年龄：</span>
                  <label for>{{currentAge}}</label>
                </li>
              </el-col>
            </ul>
          </div>
        </el-col>
      </el-row>
    </el-header>
   
    <el-main style="flex-basis:0" v-if="isShown">
      <!-- <iframe :src="talkUrl+currentId" frameborder="0" width="100%" height="100%"></iframe>-->
      <div class="container" id="container">
            <div id="timer" class="form-control p-0 mb-3" style="margin-top:100px">
              	<span id="runner">{{timeResult}}</span><br><br>
            </div>
        <div class="btn-group">
              <el-button id="start" type="primary" @click="startRecording()" :disabled="startDis">开始</el-button>
              <el-button id="stop" type="primary" @click="stopRecording()" :disabled="stopDis">停止</el-button>
            </div>
      </div>
    </el-main>
  </el-container>
</template>

<script>
import $ from 'jquery'
// import Recorder from 'recorderjs';
// import WaveSurfer from 'wavesurfer.js';
// import Microphone from 'wavesurfer.js/dist/js/wavesurfer.microphone.js';
export default {
  name: "Home",
  data() {
    return {
      userData: JSON.parse(sessionStorage.getItem("user")),
      value: "",
      pageSize: 10,
      currentPage: 1,
      patientArray: [],
      isShown: false,
      currentName: "",
      currentSex: "",
      currentAge: "",
      currentId: "",
      recorder: null,
      startDis: false,
      stopDis: true,
      playDis: true,
      talkUrl: "/robot/index.html?id=",
      hour: 0,
      minute: 0,
      seconds: 0,
      timeInterval: null,
      timeResult: null
    };
  },
  created() {
    this.getList();
  },
  methods: {
    //获取列表
    getList() {
      let _this = this;
      const userData = JSON.parse(sessionStorage.getItem("user"));
      axios({
        url: "/API/base-api/query-patient/",
        params: {
          page: _this.currentPage,
          size: _this.pageSize,
          user_id: _this.userData.id,
        },
      }).then(function (response) {
        if (!response.data.results.length) {
          _this.$router.push({ path: "/PatientInfo" });
        } else {
          _this.patientArray = response.data.results;
        }
        // _this.change(_this.$route.query.id)
      });
    },
    change(value) {
      let _this = this;
      _this.isShown = false;
     
      _this.patientArray.map((item) => {
        if (item.id == value) {
          _this.currentAge = item.patient_age;
          _this.currentName = item.patient_name;
          _this.currentSex = item.patient_sex ? "女" : "男";  
          _this.currentId = item.id;
          _this.isShown = true;
           _this.openAudio();
          sessionStorage.setItem("patient_id",item.id);
        }
      });
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
    
    },
    closeMedia() {
      let _this = this;
      _this.mediaStreamTrack && _this.mediaStreamTrack.stop();
    },
    startRecording() {
      let _this = this;
      _this.startDis = true;
      _this.stopDis = false;
      const userData = JSON.parse(sessionStorage.getItem("user"));
      let fd = new FormData();
      let userId = _this.userData.id;
      //let patient_id = _this.patientArray[0].id;
      let patient_id = sessionStorage.getItem("patient_id")
      fd.append('user_id', userId);
      fd.append('patient_id', patient_id);
      fd.append('status', '1');
      _this.timer();

      axios({
        url: "/API/voice-recorder/",
        data: fd,
        method: 'post',
      }).then(function (response) {
        if (response.data.code == 201) {
          console.log(response.data.msg);
        }
      });
    },
    stopRecording() {
      let _this = this;
      _this.startDis = false;
      _this.stopDis = true;
      const userData = JSON.parse(sessionStorage.getItem("user"));
      let fd = new FormData();
      let userId = _this.userData.id;
      //let patient_id = _this.patientArray[0].id;
      let patient_id = sessionStorage.getItem("patient_id")
      fd.append('user_id', userId);
      fd.append('patient_id', patient_id);
      fd.append('status', '0');

      clearInterval(this.timeInterval);
      this.timeInterval = null;

      axios({
        url: "/API/voice-recorder/",
        data: fd,
        method: 'post',
      }).then(function (response) {
        if (response.data.code == 202) {
          console.log(response.data.msg);
        }
      });
    },
    timer(){
      if(this.timeInterval != null){
        return
      };
      
    this.timeInterval = setInterval(() => {
        this.seconds += 1;
    if (this.seconds >= 60) {
    this.seconds = 0;
    this.minute = this.minute + 1;
    }
    
    if (this.minute >= 60) {
    this.minute = 0;
    this.hour = this.hour + 1;
    }
    this.timeResult = (this.hour < 10 ? '0' + this.hour:this.hour)+':'+(this.minute < 10 ? '0' + this.minute : this.minute) + ':' + (this.seconds < 10 ? '0' + this.seconds : this.seconds);
      }, 1000);
    },
    countSecond(){
      var oneHour = 3600000;
      var oneMinute = 60000;
      var oneSecond = 1000;
      var seconds = 0;
      var minutes = 0;
      var hours = 0;
      var result;
      var milliseconds = false;
      if (milliseconds >= oneHour) {
          hours = Math.floor(milliseconds / oneHour);
      }

      milliseconds = hours > 0 ? (milliseconds - hours * oneHour) : milliseconds;

      if (milliseconds >= oneMinute) {
          minutes = Math.floor(milliseconds / oneMinute);
      }

      milliseconds = minutes > 0 ? (milliseconds - minutes * oneMinute) : milliseconds;

      if (milliseconds >= oneSecond) {
          seconds = Math.floor(milliseconds / oneSecond);
      }

      milliseconds = seconds > 0 ? (milliseconds - seconds * oneSecond) : milliseconds;

      if (hours > 0) {
          result = (hours > 9 ? hours : "0" + hours) + ":";
      } else {
          result = "00:";
      }

      if (minutes > 0) {
          result += (minutes > 9 ? minutes : "0" + minutes) + ":";
      } else {
          result += "00:";
      }

      if (seconds > 0) {
          result += (seconds > 9 ? seconds : "0" + seconds);
      } else {
          result += "00";
      }
      return result;
    }
  },
};
</script>

<style scoped lang="scss">
.el-container {
  box-sizing: border-box;
  position: absolute;
  top: 0;
  left: 0;
  overflow-x: hidden;
  width: 100%;
  height: 100%;
  padding-top: 4rem;
  background-image: url("../assets/index-bg.jpg");
  background-size: 100% 100%;
}
.el-header,
.el-footer {
  background-color: rgba(12, 12, 12, 0.6);
  color: #333;
  text-align: center;
}
.el-main {
  color: #333;
  text-align: center;
  line-height: 100px;
  overflow-y: hidden;
}
.grid-content {
  height: 50px;
}
.grid-content span,
label {
  color: #fff;
  text-align: center;
}
.grid-content ul {
  overflow: hidden;
}
.grid-content ul li {
  list-style: none;
  float: left;
  // width: 240px;
}
.container{
    padding-right: 0;
    padding-left: 0;
}
.container div.history {
    background: #EAEAEA;
    border: 1px solid #e1e4e8;
    border-radius: 3px;
    box-shadow: inset 0 0 10px rgba(27,31,35,.05);
    padding-top: 32px;
    padding-left: 32px;
    /* height: 160px; */
    /* max-height: 366px; */
    overflow:scroll;
    overflow-x:hidden;
}
.control{
    margin-top: 1rem;
    width: 100%;
    text-align: center;
}
.CHAT2,.CHAT3{
    width: 160px;
}
button{
    justify-content: center;
}
#runner{
	font-size: 6rem;
	color: #fff;
	font-family: 'Nixie One', cursive;
	text-shadow: 0 19px 38px rgba(0,0,0,0.30), 0 15px 12px rgba(0,0,0,0.22);
}
#timer{
  
}
</style>
