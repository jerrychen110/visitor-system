(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2d2169d8"],{c2e8:function(e,s,t){"use strict";t.r(s);var a=function(){var e=this,s=e.$createElement,t=e._self._c||s;return t("el-row",[t("el-col",{staticStyle:{"padding-right":"2.4rem"},attrs:{md:24,lg:24}},[t("el-form",{ref:"form",attrs:{model:e.form,"label-position":"top"}},[t("el-card",{staticClass:"mtl",staticStyle:{display:"none"},attrs:{shadow:"never"}},[t("el-form-item",{attrs:{label:"记录id："}},[t("el-input",{model:{value:e.form.id,callback:function(s){e.$set(e.form,"id",s)},expression:"form.id"}})],1),t("el-form-item",{attrs:{label:"用户id："}},[t("el-input",{model:{value:e.form.user_id,callback:function(s){e.$set(e.form,"user_id",s)},expression:"form.user_id"}})],1)],1),t("el-card",{staticClass:"mtl",staticStyle:{display:"block"},attrs:{id:"baidu",shadow:"never"}},[t("div",{staticClass:"clearfix",attrs:{slot:"header"},slot:"header"},[t("span",[e._v("百度AI")])]),t("el-form-item",{staticStyle:{display:"none"},attrs:{label:"APP_ID："}},[t("el-input",{model:{value:e.form.id,callback:function(s){e.$set(e.form,"id",s)},expression:"form.id"}})],1),t("el-form-item",{staticStyle:{display:"none"},attrs:{label:"APP_ID："}},[t("el-input",{model:{value:e.form.user_id,callback:function(s){e.$set(e.form,"user_id",s)},expression:"form.user_id"}})],1),t("el-form-item",{attrs:{label:"App Id："}},[t("el-input",{model:{value:e.form.baidu_app_id,callback:function(s){e.$set(e.form,"baidu_app_id",s)},expression:"form.baidu_app_id"}})],1),t("el-form-item",{attrs:{label:"Api Key："}},[t("el-input",{model:{value:e.form.baidu_app_key,callback:function(s){e.$set(e.form,"baidu_app_key",s)},expression:"form.baidu_app_key"}})],1),t("el-form-item",{attrs:{label:"Secret Key："}},[t("el-input",{model:{value:e.form.baidu_secret_key,callback:function(s){e.$set(e.form,"baidu_secret_key",s)},expression:"form.baidu_secret_key"}})],1),t("el-form-item",{attrs:{label:"Robot Id(百度UNIT机器人ID)："}},[t("el-input",{model:{value:e.form.baidu_service_id,callback:function(s){e.$set(e.form,"baidu_service_id",s)},expression:"form.baidu_service_id"}})],1)],1),t("el-card",{staticClass:"mtl",staticStyle:{display:"none"},attrs:{id:"tencent",shadow:"never"}},[t("div",{staticClass:"clearfix",attrs:{slot:"header"},slot:"header"},[t("span",[e._v("腾讯AI")])]),t("el-form-item",{attrs:{label:"Secret Id："}},[t("el-input",{model:{value:e.form.tencent_secret_id,callback:function(s){e.$set(e.form,"tencent_secret_id",s)},expression:"form.tencent_secret_id"}})],1),t("el-form-item",{attrs:{label:"Secret Key："}},[t("el-input",{model:{value:e.form.tencent_secret_key,callback:function(s){e.$set(e.form,"tencent_secret_key",s)},expression:"form.tencent_secret_key"}})],1)],1),t("el-card",{staticClass:"mtl",staticStyle:{display:"none"},attrs:{id:"face",shadow:"never"}},[t("div",{staticClass:"clearfix",attrs:{slot:"header"},slot:"header"},[t("span",[e._v("旷视AI")])]),t("el-form-item",{attrs:{label:"Api Key："}},[t("el-input",{model:{value:e.form.face_api_key,callback:function(s){e.$set(e.form,"face_api_key",s)},expression:"form.face_api_key"}})],1),t("el-form-item",{attrs:{label:"Api Secret："}},[t("el-input",{model:{value:e.form.face_api_secret,callback:function(s){e.$set(e.form,"face_api_secret",s)},expression:"form.face_api_secret"}})],1)],1),t("el-card",{staticClass:"mtl",staticStyle:{display:"none"},attrs:{id:"xfyun",shadow:"never"}},[t("div",{staticClass:"clearfix",attrs:{slot:"header"},slot:"header"},[t("span",[e._v("讯飞AI")])]),t("el-form-item",{attrs:{label:"Api Key："}},[t("el-input",{model:{value:e.form.xfyun_api_key,callback:function(s){e.$set(e.form,"xfyun_api_key",s)},expression:"form.xfyun_api_key"}})],1),t("el-form-item",{attrs:{label:"Api Secret："}},[t("el-input",{model:{value:e.form.xfyun_api_secret,callback:function(s){e.$set(e.form,"xfyun_api_secret",s)},expression:"form.xfyun_api_secret"}})],1)],1),t("el-card",{staticStyle:{display:"none"},attrs:{id:"zhiyun",shadow:"never"}},[t("div",{staticClass:"clearfix",attrs:{slot:"header"},slot:"header"},[t("span",[e._v("智云网关")])]),t("el-row",{attrs:{gutter:20}},[t("el-col",{attrs:{span:12}},[t("el-form-item",{attrs:{label:"ZHIYUN_ID："}},[t("el-input",{model:{value:e.form.zhiyun_id,callback:function(s){e.$set(e.form,"zhiyun_id",s)},expression:"form.zhiyun_id"}})],1)],1),t("el-col",{attrs:{span:12}},[t("el-form-item",{attrs:{label:"ZHIYUN_SERVER："}},[t("el-input",{model:{value:e.form.zhiyun_server,callback:function(s){e.$set(e.form,"zhiyun_server",s)},expression:"form.zhiyun_server"}})],1)],1),t("el-col",{attrs:{span:12}},[t("el-form-item",{attrs:{label:"ZHIYUN_KEY："}},[t("el-input",{model:{value:e.form.zhiyun_key,callback:function(s){e.$set(e.form,"zhiyun_key",s)},expression:"form.zhiyun_key"}})],1)],1),t("el-col",{attrs:{span:12}})],1),t("el-row",{staticStyle:{"margin-top":"10px"}},[t("el-col",{attrs:{span:6,offset:9}},[t("el-button",{staticClass:"w-100",style:{display:e.visibleConnect},attrs:{id:"aid_save",type:"primary"},on:{click:function(s){return e.connect()}}},[e._v("连接")]),t("el-button",{staticClass:"w-100",style:{display:e.visibleDisConnect},attrs:{id:"aid_disconnect",type:"primary"},on:{click:function(s){return e.disconnect()}}},[e._v("断开")])],1)],1),t("el-row",{attrs:{gutter:20}},[t("el-col",{attrs:{span:12}},[t("el-form-item",{attrs:{label:"SENSOR_A_MAC："}},[t("el-input",{model:{value:e.form.sensor_a_mac,callback:function(s){e.$set(e.form,"sensor_a_mac",s)},expression:"form.sensor_a_mac"}})],1)],1),t("el-col",{attrs:{span:12}},[t("el-form-item",{attrs:{label:"SENSOR_B_MAC："}},[t("el-input",{model:{value:e.form.sensor_b_mac,callback:function(s){e.$set(e.form,"sensor_b_mac",s)},expression:"form.sensor_b_mac"}})],1)],1),t("el-col",{attrs:{span:12}},[t("el-form-item",{attrs:{label:"SENSOR_C_MAC："}},[t("el-input",{model:{value:e.form.sensor_c_mac,callback:function(s){e.$set(e.form,"sensor_c_mac",s)},expression:"form.sensor_c_mac"}})],1)],1),t("el-col",{attrs:{span:12}},[t("el-form-item",{attrs:{label:"SENSOR_D_MAC："}},[t("el-input",{model:{value:e.form.sensor_d_mac,callback:function(s){e.$set(e.form,"sensor_d_mac",s)},expression:"form.sensor_d_mac"}})],1)],1),t("el-col",{attrs:{span:12}},[t("el-form-item",{attrs:{label:"SENSOR_EH_MAC："}},[t("el-input",{model:{value:e.form.sensor_eh_mac,callback:function(s){e.$set(e.form,"sensor_eh_mac",s)},expression:"form.sensor_eh_mac"}})],1)],1),t("el-col",{attrs:{span:12}},[t("el-form-item",{attrs:{label:"SENSOR_EL_MAC："}},[t("el-input",{model:{value:e.form.sensor_el_mac,callback:function(s){e.$set(e.form,"sensor_el_mac",s)},expression:"form.sensor_el_mac"}})],1)],1)],1)],1),t("el-row",{staticStyle:{"margin-top":"10px"}},[t("el-col",{attrs:{span:6,offset:9}},[t("el-button",{staticClass:"w-100",attrs:{type:"primary"},on:{click:function(s){return e.onSubmit("form")}}},[e._v("保存修改")])],1)],1)],1)],1)],1)},n=[],r=(t("28a5"),t("f499")),o=t.n(r),i=function(e,s){var t=this;t.uid=e,t.key=s,t.saddr="api.zhiyun360.com:28090",t.onConnect=null,t.onConnectLost=null,t.onmessageArrive=null,t.setIdKey=function(e,s){t.uid=e,t.key=s},t.initZCloud=function(e,s){t.uid=e,t.key=s},t.setServerAddr=function(e){t.saddr=e},t.disconnect=function(){t.wsc&&t.wsc.close()},t.connect=function(){t.wsc=new WebSocket("wss://"+t.saddr),t.wsc.onopen=function(e){var s={method:"authenticate",uid:t.uid,key:t.key},a=o()(s);t.wsc.send(a),t.onConnect&&t.onConnect()},t.wsc.onmessage=function(e){var s=JSON.parse(e.data);s.method&&s.addr&&s.data&&"message"==s.method&&t.onmessageArrive&&t.onmessageArrive(s.addr,s.data)},t.wsc.onclose=function(){t.onConnectLost&&t.onConnectLost()}},t.sendMessage=function(e,s){var a={method:"control",addr:e,data:s},n=o()(a);t.wsc.send(n)}},c=t("1157"),l=t.n(c),m={name:"Edit",data:function(){return{labelPosition:"top",visibleConnect:"",visibleDisConnect:"none",form:{id:null,zhiyun_id:"",zhiyun_server:"",zhiyun_key:"",sensor_a_mac:"",sensor_b_mac:"",sensor_c_mac:"",sensor_d_mac:"",sensor_eh_mac:"",sensor_el_mac:"",baidu_app_id:"",baidu_app_key:"",baidu_secret_key:"",baidu_service_id:"",tencent_secret_id:"",tencent_secret_key:"",face_api_key:"",face_api_secret:"",xfyun_api_key:"",xfyun_api_secret:"",user_id:null},rtc:new i,mac2type:{},mac2sensor:{},type2mac:{},macs:{},flag_typeArr:[],ioffset:0,lost_num:0,lost_timer:null,reconnect_timer:null,isHandLost:!1}},created:function(){this.getData(),this.rtc.onConnect=this.onConnect,this.rtc.onConnectLost=this.onConnectLost,this.rtc.onmessageArrive=this.onmessageArrive,this.rtc._connect=!1},methods:{getData:function(){var e=this,s=JSON.parse(sessionStorage.getItem("user")),t=s.id;axios.get("/API/sys-parameters-manage/",{params:{userId:t}}).then(function(s){e.form=s.data.result_data,e.form.zhiyun_server="api.zhiyun360.com:28090"})},handleTab:function(e){var s=e.index;0==s?(l()("#zhiyun").show(),l()("#baidu").hide(),l()("#tencent").hide(),l()("#face").hide(),l()("#xfyun").hide()):1==s?(l()("#zhiyun").hide(),l()("#baidu").show(),l()("#tencent").hide(),l()("#face").hide(),l()("#xfyun").hide()):2==s?(l()("#zhiyun").hide(),l()("#baidu").hide(),l()("#tencent").show(),l()("#face").hide(),l()("#xfyun").hide()):3==s?(l()("#zhiyun").hide(),l()("#baidu").hide(),l()("#tencent").hide(),l()("#face").show(),l()("#xfyun").hide()):4==s&&(l()("#zhiyun").hide(),l()("#baidu").hide(),l()("#tencent").hide(),l()("#face").hide(),l()("#xfyun").show()),l()("#aid_disconnect").click()},connect:function(){var e=this;e.form.zhiyun_id&&e.form.zhiyun_key&&e.form.zhiyun_server?(e.rtc.setIdKey(e.form.zhiyun_id,e.form.zhiyun_key),e.rtc.setServerAddr(e.form.zhiyun_server),e.rtc.connect(),console.log("%c 建立连接","color:red"),e.$message({message:"已成功建立连接！",type:"success"}),e.onSubmit("form")):e.$message({message:"ZHIYUN_ID、ZHIYUN_KEY、ZHIYUN_SERVER必须填写",type:"error"})},disconnect:function(){var e=this;e.rtc._connect&&(e.rtc.disconnect(),e.isHandLost=!0,e.$message({message:"已成功断开连接！",type:"success"}))},onConnect:function(){var e=this;console.log("已连接到"+e.form.zhiyun_id),e.rtc.sendMessage("FF:FF:FF:FF:FF:FF:FF:FF","{TYPE=?,A0=?,A1=?,A2=?,A3=?,A4=?,A5=?,A6=?,D1=?}"),e.rtc._connect=!0,e.ioffset=0,e.flag_typeArr=[],e.visibleConnect="none",e.visibleDisConnect=""},onConnectLost:function(){var e=this;if(e.rtc._connect=!1,e.visibleConnect="",e.visibleDisConnect="none",!e.isHandLost){var s=3;e.reconnect_timer=setInterval(function(){s--,s>0&&console.log("连接断开，"+s+"秒后重新连接"),e.$message({message:"连接已断开,"+s+"秒后重新连接",type:"error"})},1e3),e.lost_timer=setTimeout(function(){e.reconnect_timer&&clearInterval(e.reconnect_timer),l()("#aid_save").click(),e.lost_num++},3e3)}},onmessageArrive:function(e,s){var t=this;if("{"==s[0]&&"}"==s[s.length-1]){s=s.substr(1,s.length-2);for(var a=s.split(","),n=0;n<a.length;n++){var r=a[n].split("=");if(2==r.length){var o=r[0],i=r[1];if("PN"==o)return;if("TYPE"==o){var c=i.substr(2,3);console.log("type:"+c+"||mac:"+e),"601"==c?(t.form.sensor_a_mac=e,null!=t.form.sensor_a_mac&&""!=t.form.sensor_a_mac||t.$message({message:"A类节点成功上线！",type:"success"})):"602"==c?(t.form.sensor_b_mac=e,null!=t.form.sensor_b_mac&&""!=t.form.sensor_b_mac||t.$message({message:"B类节点成功上线！",type:"success"})):"603"==c?(t.form.sensor_c_mac=e,null!=t.form.sensor_c_mac&&""!=t.form.sensor_c_mac||t.$message({message:"C类节点成功上线！",type:"success"})):"604"==c?(t.form.sensor_d_mac=e,null!=t.form.sensor_d_mac&&""!=t.form.sensor_d_mac||t.$message({message:"D类节点成功上线！",type:"success"})):"605"==c?(t.form.sensor_eh_mac=e,null!=t.form.sensor_eh_mac&&""!=t.form.sensor_eh_mac||t.$message({message:"EH类节点成功上线！",type:"success"})):"606"==c&&(t.form.sensor_el_mac=e,null!=t.form.sensor_el_mac&&""!=t.form.sensor_el_mac||t.$message({message:"EL类节点成功上线！",type:"success"}))}}}}},onSubmit:function(e){var s=this;s.$refs[e].validate(function(e){if(!e)return!1;if(null==s.form.user_id){var t=JSON.parse(sessionStorage.getItem("user")),a=t.id;s.form.user_id=a}axios({url:"/API/sys-parameters-manage/",data:s.form,method:"post",headers:{"Hide-Message":!0}}).then(function(){s.$message({message:"修改成功！",type:"success"})})})}}},_=m,f=t("2877"),u=Object(f["a"])(_,a,n,!1,null,null,null);s["default"]=u.exports}}]);
//# sourceMappingURL=chunk-2d2169d8.5a2cde31.js.map