<template>
  <el-row>
    <el-col :md="24" :lg="24" style="padding-right: 2.4rem;">
      <el-form ref="form" :model="form" label-position="top">
        <!--<el-tabs type="card" @tab-click="handleTab">
          <el-tab-pane key="1" label="智云服务"></el-tab-pane>
          <el-tab-pane key="2" label="百度AI"></el-tab-pane>
          <el-tab-pane key="3" label="腾讯AI"></el-tab-pane>
          <el-tab-pane key="4" label="旷视AI"></el-tab-pane>
          <el-tab-pane key="5" label="讯飞AI"></el-tab-pane>
        </el-tabs>-->

        <el-card shadow="never" class="mtl" style="display:none">
          <el-form-item label="记录id：">
            <el-input v-model="form.id"></el-input>
          </el-form-item>
          <el-form-item label="用户id：">
            <el-input v-model="form.user_id"></el-input>
          </el-form-item>
        </el-card>


        <el-card id="baidu" shadow="never" class="mtl" style="display:block">
          <div slot="header" class="clearfix">
            <span>百度AI</span>
          </div>
            <el-form-item label="APP_ID：" style="display:none">
              <el-input v-model="form.id"></el-input>
            </el-form-item>
            <el-form-item label="APP_ID：" style="display:none">
              <el-input v-model="form.user_id"></el-input>
            </el-form-item>
            <el-form-item label="App Id：">
              <el-input v-model="form.baidu_app_id"></el-input>
            </el-form-item>
            <el-form-item label="Api Key：">
              <el-input v-model="form.baidu_app_key"></el-input>
            </el-form-item>
            <el-form-item label="Secret Key：">
              <el-input v-model="form.baidu_secret_key"></el-input>
            </el-form-item>
            <el-form-item label="Robot Id(百度UNIT机器人ID)：">
              <el-input v-model="form.baidu_service_id"></el-input>
            </el-form-item>
        </el-card>

        <el-card id="tencent" shadow="never" class="mtl" style="display:none">
          <div slot="header" class="clearfix">
            <span>腾讯AI</span>
          </div>
            <el-form-item label="Secret Id：">
              <el-input v-model="form.tencent_secret_id"></el-input>
            </el-form-item>
            <el-form-item label="Secret Key：">
              <el-input v-model="form.tencent_secret_key"></el-input>
            </el-form-item>
        </el-card>

        <el-card id="face" shadow="never" class="mtl" style="display:none">
          <div slot="header" class="clearfix">
            <span>旷视AI</span>
          </div>
            <el-form-item label="Api Key：">
              <el-input v-model="form.face_api_key"></el-input>
            </el-form-item>
            <el-form-item label="Api Secret：">
              <el-input v-model="form.face_api_secret"></el-input>
            </el-form-item>
        </el-card>

        <el-card id="xfyun" shadow="never" class="mtl" style="display:none">
          <div slot="header" class="clearfix">
            <span>讯飞AI</span>
          </div>
            <el-form-item label="Api Key：">
              <el-input v-model="form.xfyun_api_key"></el-input>
            </el-form-item>
            <el-form-item label="Api Secret：">
              <el-input v-model="form.xfyun_api_secret"></el-input>
            </el-form-item>
        </el-card>

        <el-card id="zhiyun" shadow="never" style="display:none">
          <div slot="header" class="clearfix">
            <span>智云网关</span>
          </div>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="ZHIYUN_ID：">
                  <el-input v-model="form.zhiyun_id"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="ZHIYUN_SERVER：">
                  <el-input v-model="form.zhiyun_server"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="ZHIYUN_KEY：">
                  <el-input v-model="form.zhiyun_key"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                
              </el-col>
            </el-row>
            <el-row style="margin-top: 10px">
              <el-col :span="6" :offset="9">
                <el-button id="aid_save" type="primary" class="w-100" @click="connect()" :style="{ display: visibleConnect }">连接</el-button>
                <el-button id="aid_disconnect" type="primary" class="w-100" @click="disconnect()" :style="{ display: visibleDisConnect }">断开</el-button>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="SENSOR_A_MAC：">
                  <el-input v-model="form.sensor_a_mac"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="SENSOR_B_MAC：">
                  <el-input v-model="form.sensor_b_mac"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="SENSOR_C_MAC：">
                  <el-input v-model="form.sensor_c_mac"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="SENSOR_D_MAC：">
                  <el-input v-model="form.sensor_d_mac"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="SENSOR_EH_MAC：">
                  <el-input v-model="form.sensor_eh_mac"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="SENSOR_EL_MAC：">
                  <el-input v-model="form.sensor_el_mac"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
        </el-card>
        <el-row style="margin-top: 10px">
          <el-col :span="6" :offset="9">
            <el-button type="primary" class="w-100" @click="onSubmit('form')">保存修改</el-button>
          </el-col>
        </el-row>
      </el-form>
    </el-col>
  </el-row>
</template>

<script>
import {WSNRTConnect} from '@/assets/js/WSNRTConnect.js';
import $ from 'jquery'

export default {
  name: "Edit",
  data() {
    return {
      labelPosition: 'top',
      visibleConnect: '',
      visibleDisConnect: 'none',
      form: {
        id: null,
        zhiyun_id: '',
        zhiyun_server: '',
        zhiyun_key: '',
        sensor_a_mac: '',
        sensor_b_mac: '',
        sensor_c_mac: '',
        sensor_d_mac: '',
        sensor_eh_mac: '',
        sensor_el_mac: '',
        baidu_app_id: '',
        baidu_app_key: '',
        baidu_secret_key: '',
        baidu_service_id: '',
        tencent_secret_id: '',
        tencent_secret_key: '',
        face_api_key: '',
        face_api_secret: '',
        xfyun_api_key: '',
        xfyun_api_secret: '',
        user_id: null
      },
        rtc: new WSNRTConnect(),
        mac2type: {},
        mac2sensor: {},
        type2mac: {},
        macs: {},
        flag_typeArr: [],
        ioffset: 0,
        lost_num: 0,
        lost_timer: null,
        reconnect_timer: null,
        isHandLost: false
    }
  },
  created (){
    this.getData();
    this.rtc.onConnect = this.onConnect;
    this.rtc.onConnectLost = this.onConnectLost;
    this.rtc.onmessageArrive = this.onmessageArrive;
    this.rtc._connect = false;

  },
  methods: {
    //获取数据
    getData(){
      let _this = this;
      const userData = JSON.parse(sessionStorage.getItem('user'));
      let userId = userData.id;
      axios.get('/API/sys-parameters-manage/', {params:{'userId': userId}}).then( res => {
        _this.form = res.data.result_data;
        _this.form.zhiyun_server = "api.zhiyun360.com:28090";
      })
    },
    handleTab(tab) {
      let _this = this;
      let tabIndex = tab.index;
      if(tabIndex==0){
        $("#zhiyun").show();
        $("#baidu").hide();
        $("#tencent").hide();
        $("#face").hide();
        $("#xfyun").hide();
      }else if(tabIndex==1){
        $("#zhiyun").hide();
        $("#baidu").show();
        $("#tencent").hide();
        $("#face").hide();
        $("#xfyun").hide();
      }else if(tabIndex==2){
        $("#zhiyun").hide();
        $("#baidu").hide();
        $("#tencent").show();
        $("#face").hide();
        $("#xfyun").hide();
      }else if(tabIndex==3){
        $("#zhiyun").hide();
        $("#baidu").hide();
        $("#tencent").hide();
        $("#face").show();
        $("#xfyun").hide();
      }else if(tabIndex==4){
        $("#zhiyun").hide();
        $("#baidu").hide();
        $("#tencent").hide();
        $("#face").hide();
        $("#xfyun").show();
      }
      $("#aid_disconnect").click();
    },
    connect() {
        let _this = this;
        if(_this.form.zhiyun_id&&_this.form.zhiyun_key&&_this.form.zhiyun_server){
          _this.rtc.setIdKey(_this.form.zhiyun_id, _this.form.zhiyun_key);
          _this.rtc.setServerAddr(_this.form.zhiyun_server);
          _this.rtc.connect();
          console.log("%c 建立连接", "color:red");
          _this.$message({message: '已成功建立连接！', type: 'success'});
          _this.onSubmit('form');
        }else{
          _this.$message({message: 'ZHIYUN_ID、ZHIYUN_KEY、ZHIYUN_SERVER必须填写', type: 'error'});
        }
    },
    disconnect(){
        let _this = this;
        if(_this.rtc._connect){
            _this.rtc.disconnect();
            _this.isHandLost = true;
            _this.$message({message: '已成功断开连接！', type: 'success'});
        }
    },
    onConnect(){
        let _this = this;
        console.log('已连接到'+_this.form.zhiyun_id);
        _this.rtc.sendMessage("FF:FF:FF:FF:FF:FF:FF:FF", "{TYPE=?,A0=?,A1=?,A2=?,A3=?,A4=?,A5=?,A6=?,D1=?}");
        _this.rtc._connect=true;
        _this.ioffset = 0;
        _this.flag_typeArr = [];
        _this.visibleConnect = 'none';
        _this.visibleDisConnect = '';
    },
    onConnectLost(){
      let _this = this;
      _this.rtc._connect = false;
      _this.visibleConnect = '';
      _this.visibleDisConnect = 'none';
      if(!_this.isHandLost) {
          var num = 3;
          _this.reconnect_timer = setInterval(function () {
              num--;
              if (num > 0)
                  console.log('连接断开，' + num + '秒后重新连接');
                  _this.$message({message: '连接已断开,' + num + '秒后重新连接', type: 'error'});
          }, 1000)
          _this.lost_timer = setTimeout(function () {
              if (_this.reconnect_timer)
                  clearInterval(_this.reconnect_timer);
              $("#aid_save").click();
              _this.lost_num++;
          }, 3000);
      }
    },
    onmessageArrive(mac, dat) {
        let _this = this;
        if (dat[0]=='{' && dat[dat.length-1]=='}') {
            dat = dat.substr(1, dat.length-2);
            var its = dat.split(',');
            for (var i=0; i<its.length; i++) {
                var it = its[i].split('=');
                if (it.length == 2) {
                    var tag = it[0];
                    var val = it[1];
                    if(tag=="PN")return;
                    if(tag == "TYPE") {
                        var t = val.substr(2,3);
                        console.log("type:"+t+"||"+"mac:"+mac);
                        if(t=="601"){
                            _this.form.sensor_a_mac = mac;
                            if(_this.form.sensor_a_mac==null||_this.form.sensor_a_mac==''){
                              _this.$message({message: 'A类节点成功上线！', type: 'success'});
                            }
                        }else if(t=="602"){
                            _this.form.sensor_b_mac = mac;
                            if(_this.form.sensor_b_mac==null||_this.form.sensor_b_mac==''){
                              _this.$message({message: 'B类节点成功上线！', type: 'success'});
                            }
                        }else if(t=="603"){
                            _this.form.sensor_c_mac = mac;
                            if(_this.form.sensor_c_mac==null||_this.form.sensor_c_mac==''){
                              _this.$message({message: 'C类节点成功上线！', type: 'success'});
                            }
                        }else if(t=="604"){
                            _this.form.sensor_d_mac = mac;
                            if(_this.form.sensor_d_mac==null||_this.form.sensor_d_mac==''){
                              _this.$message({message: 'D类节点成功上线！', type: 'success'});
                            }
                        }else if(t=="605"){
                            _this.form.sensor_eh_mac = mac;
                            if(_this.form.sensor_eh_mac==null||_this.form.sensor_eh_mac==''){
                              _this.$message({message: 'EH类节点成功上线！', type: 'success'});
                            }
                        }else if(t=="606"){
                            _this.form.sensor_el_mac = mac;
                            if(_this.form.sensor_el_mac==null||_this.form.sensor_el_mac==''){
                              _this.$message({message: 'EL类节点成功上线！', type: 'success'});
                            }
                        }
                    }
                }
            }
        }
    },
    //提交
    onSubmit(formName) {
      let _this = this;
      _this.$refs[formName].validate((valid) => {
        if (valid) {
          if(_this.form.user_id==null){
            const userData = JSON.parse(sessionStorage.getItem('user'));
            let userId = userData.id;
            _this.form.user_id=userId;
          }
          // 接口
          axios({
            url: '/API/sys-parameters-manage/',
            data: _this.form,
            method: 'post',
            headers: {'Hide-Message': true}
          }).then(()=>{
            _this.$message({message: '修改成功！', type: 'success'});
          })
        } else {
          return false;
        }
      });
    }
  }
}
</script>