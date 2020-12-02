<template>
  <div class="bg login-bg flex-center">
    <div style="height: 80%; width: 70%;">
      <el-row :gutter="24" class="list-index-card">
        <el-col :span="6" v-for="(item, index) in tableData" :key="index">
          <div class="flex-center index-card" :style="'background-color:'+colorArr[index]" @click="goUrl(item.user.username, item.app_url)">
            <div class="w-100">
              <img :src="require('@/assets/appIcon/svg-icon-'+item.logo+'.svg')" name="" />
              <span>{{ item.app_name }}</span>
            </div>
            <div class="ele">
              <div class="mask" v-if="item.isShow">
                <qriously :value="item.android" :size="150"/>
              </div>
            </div>
            <div class="download" v-if="item.android!=''&&item.android!=null" @mouseover='showImg(item)' @mouseout='hideImg(item)'/>
            <div class="user-name-box">
              <div class="user-name" :style="'color:'+Color_HSL_L(colorArr[index])">{{ item.user.first_name }}</div>
            </div>
          </div>
        </el-col>
        <el-col v-if="tableData.length==0">
          <div class="flex-center h-100">
            <img src="@/assets/no-data.png" alt="">
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col class="apps-pagination">
          <el-pagination
            background
            layout="prev, pager, next"
            :hide-on-single-page="true"
            @current-change="currentChange"
            :page-size="this.pageSize"
            :current-page="this.currentPage"
            :total="this.count">
          </el-pagination>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import  { shuffle, Color_HSL_L }  from '@/plugins/components.js'

export default {
  name: 'List',
  data (){
    return {
      // query: '',
      pageSize: 8,
      currentPage: 1,
      count: null,
      tableData: [],
      colorArr: [
        'hsl(175, 64%, 50%)',
        'hsl(203, 76%, 49%)',
        'hsl(237, 100%, 70%)',
        'hsl(38, 91%, 44%)',
        'hsl(301, 71%, 58%)',
        'hsl(257, 100%, 68%)',
        'hsl(324, 73%, 47%)',
        'hsl(211, 87%, 56%)',
        'hsl(13, 90%, 69%)',
        'hsl(120, 55%, 52%)',
        'hsl(213, 66%, 50%)',
        'hsl(254, 77%, 55%)'
      ],
      theader: [{
        prop: 'app_name',
        label: '应用名称'
      },{
        prop: 'app_url',
        label: '应用URL'
      }]
    }
  },
  created (){
    this.getList();
  },
  methods: {
    //洗牌
    shuffle: shuffle,
    //hsl颜色明暗
    Color_HSL_L: Color_HSL_L,
    //跳转
    goUrl(username, url){
        if(username&&url){
            window.open(document.location.protocol + '//' + window.location.host + '/apps/' + username + url);
        }else{
            let _this = this;
            _this.$message({
              type: 'warning',
              message: '请创建应用!',
              duration: 2000
            });
        }
    },
    //获取列表
    getList (){
      let _this = this;
      _this.colorArr = _this.shuffle(_this.colorArr);
      axios({
        url: '/API/base-api/query-app/',
        params: {
          page: _this.currentPage,
          // app_name: _this.query
        }
      }).then(function (response) {
        _this.tableData = response.data.results;
        _this.count = response.data.results.length;
        let arr = response.data.results;
        _this.appListCount = arr.length;
        for (let index = 0; index < _this.appListCount; index++) {
          var android_file = arr[index].android_file;
          if(android_file!=null&&android_file!=''&&android_file.indexOf('/')!=0){
              var file_arr = android_file.split('/');
              android_file = file_arr[0]+'/'+file_arr[1]+'/'+file_arr[2]+'/'+file_arr[file_arr.length-5]+'/'+file_arr[file_arr.length-4]+'/'+file_arr[file_arr.length-3]+'/'+file_arr[file_arr.length-2]+'/'+file_arr[file_arr.length-1];
          }
          _this.tableData[index].android = android_file;
          _this.tableData[index].isShow = false;
        }
        var maxPage = Math.ceil(_this.count/8);
        if(_this.currentPage==maxPage){
            var add = 8 - _this.tableData.length;
            var item = {app_name:"创建应用",logo:"default",app_url:"",user:{first_name:""},android:null,isShow:false};
            for(var i=0;i<add;i++){
              _this.tableData.push(item);
            }
        }
      })
    },
    showImg(item){
      item.isShow = true;
    },
    hideImg(item){
     item.isShow = false
    },
    //翻页
    currentChange (val){
      this.currentPage = val;
      this.getList();
    },
    //
    showEllipsis (obj){
      return obj.scrollWidth > obj.clientWidth?true:false
    }
  }
}
</script>

<style scoped lang="scss">
.list-index-card{
  display: flex;
  flex-wrap: wrap;
  height: 100%;
  color: white;
  text-align: center;
  .index-card{
    position: relative;
    height: calc(100% - 24px);
    background-color: gray;
    cursor:pointer;
    img{
      height: 85px;
    }
    span{
      overflow:hidden;
      white-space:nowrap;
      text-overflow:ellipsis;
      display: block;
      box-sizing: border-box;
      margin-bottom: 1rem;
      padding: .5rem 1rem;
      width: 100%;
      font-size: 1.375rem;
    }
    .user-name-box{
      position: absolute;
      bottom: 0;
      width: 60%;
      height: 1.75rem;
      line-height: 1.75rem;
      background: #ffffff80;
      &:before,
      &:after{
        position: absolute;
        left: -1rem;
        bottom: 0;
        content:"";
        display:block;
        width:0;
        height:0;
        border-width:0px 0px 1.75rem 1rem;
        border-style:none solid solid;
        border-color:transparent transparent #ffffff80;
      }
      &:after{
        left: auto;
        right: -1rem;
        border-width: 0px 1rem 1.75rem 0px ;
      }
      .user-name{
        overflow:hidden;
        white-space:nowrap;
        text-overflow:ellipsis;
      }
    }
  }
}

.ele {
  //cursor:pointer;
  .mask{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(125, 59, 118, 1);
    color: #ffffff;
    opacity: 1;
  }
}
/*.ele:hover .mask {*/
  /*opacity: 1;*/
/*}*/

.download{
    position: absolute;
    right: 0;
    bottom: 0;
    width: 50px;
    height: 50px;
    text-indent: -9999px;
    background: url(../../../assets/qrcode.png) no-repeat 11px 10px #228fbd;
    border-radius: 60% 0 0 0;
    cursor: pointer;
    z-index: 10;
}
.mask div{
  margin:40px auto;
}
</style>

<style lang="scss">
.apps-pagination{
  text-align: center;
  .el-pagination.is-background{
    .btn-prev,
    .btn-next,
    .el-pager li{
      color: white;
      background-color: transparent;
      border-radius: 50%;
    }
  }
}
</style>