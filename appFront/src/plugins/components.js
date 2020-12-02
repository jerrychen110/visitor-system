import Router from '@/router';

//日期格式化
let dateFormat = function(fmt, date) { //meizz
  date = new Date(date);
  let o = {   
    "M+" : date.getMonth()+1,                 //月份   
    "d+" : date.getDate(),                    //日   
    "h+" : date.getHours(),                   //小时   
    "m+" : date.getMinutes(),                 //分   
    "s+" : date.getSeconds(),                 //秒   
    "q+" : Math.floor((date.getMonth()+3)/3), //季度   
    "S"  : date.getMilliseconds()             //毫秒   
  };   
  if(/(y+)/.test(fmt))   
    fmt=fmt.replace(RegExp.$1, (date.getFullYear()+"").substr(4 - RegExp.$1.length));   
  for(let k in o)   
    if(new RegExp("("+ k +")").test(fmt))   
  fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));   
  return fmt;   
}

//日期格式化
let createdFormat = function(row, column, cellValue) { //row, column, cellValue, index
  return dateFormat('yyyy-MM-dd hh:mm:ss', cellValue)
}

//是否公有格式化
let publicFormat = function(row, column, cellValue) { //row, column, cellValue, index
  return cellValue?'公有':'私有'
}
let patientSex = function(row, column, cellValue) { //row, column, cellValue, index
  return cellValue?'女':'男'
}
//设备状态
let devStatusFormat = function(row, column, cellValue) { //row, column, cellValue, index
  if (cellValue == 0){
    return '离线'
  }
  else if (cellValue == 1){
    return '在线'
  }
}

//页面跳转
let handleJump = function(url, id){
  id = id?id:'';
  Router.push({ path: url + id });
}
//页面跳转
let handleJump2 = function(url, id){
  id = id?id:'';
  Router.push({ path: url, query: {id:id}});
}

//洗牌
let shuffle = function(input) {
  for (var i = input.length-1; i >=0; i--) {
      var randomIndex = Math.floor(Math.random()*(i+1));
      var itemAtIndex = input[randomIndex];
      input[randomIndex] = input[i];
      input[i] = itemAtIndex;
  }
  return input;
}

//hsl颜色明暗
let Color_HSL_L = function(str, val) {
  val = val?val:-10;
  var L = Number(str.slice(-5,-2));
  var newStr = str.slice(0,-4) + String(L+val) + str.slice(-2);
  return newStr
}

//获取cookie
let getCookie = function(name) {
  let value = '; ' + document.cookie
  let parts = value.split('; ' + name + '=')
  if (parts.length === 2) return parts.pop().split(';').shift()
}

//设置cookie
let setCookie = function(name,value, days) {
  let exp = new Date();
  exp.setTime(exp.getTime() + days*24*60*60*1000);
  document.cookie = name + "="+ escape (value) + ";expires=" + exp.toGMTString();
}

export {
  dateFormat,
  createdFormat,
  publicFormat,
  patientSex,
  devStatusFormat,
  handleJump,
  handleJump2,
  shuffle,
  Color_HSL_L,
  getCookie,
  setCookie
}