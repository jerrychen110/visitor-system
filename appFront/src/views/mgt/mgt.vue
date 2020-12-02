<template>
  <div>
    <el-container>
      <el-header class="header">
        <!-- <img class="logo" src="@/assets/logo.png"> -->
        <h1>{{this.$route.matched[0].meta.title}}</h1>
        <el-button type="primary" size="mini" class="header-back-btn" @click="handleJump('/')">返回首页</el-button>
        <div class="header-user">
          <el-dropdown @command="handleCommand">
            <span class="el-dropdown-link">
              <i class="el-icon-user-solid"></i>
              {{ username }}
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item :command="{url:'UserInfo',name:'编辑信息'}">编辑信息</el-dropdown-item>
              <el-dropdown-item :command="{url:'Password',name:'修改密码'}">修改密码</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
      </el-header>
      
      <el-container>
        <el-aside :width="asideWidth">
          <el-menu :default-active="this.$route.path" router class="el-menu-vertical-demo aside" :collapse="isCollapse">
            <el-menu-item :index="item.index" v-for="item in navList" :key="item.index">
              <i :class="item.icon"></i>
              <span slot="title">{{ item.title }}</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main class="main">
          <el-row>
            <el-col :span="24" class="mbl">
              <el-breadcrumb separator="/">
                <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
                <el-breadcrumb-item>管理平台</el-breadcrumb-item>
                <el-breadcrumb-item
                  v-for="item in filterBreadcrumb"
                  :key="item.id">
                  {{ item.meta.title }}
                </el-breadcrumb-item>
              </el-breadcrumb>
            </el-col>
          </el-row>
          <!-- router-view -->
          <router-view/>
          <!-- router-view -->
        </el-main>
      </el-container>
    </el-container>
    <dialogs :show.sync="dialogVisible" :req-data="dialogReqData"></dialogs>
  </div>
</template>

<script>
import mgtRouter from './router'
import  { handleJump }  from '@/plugins/components.js'
import  dialogs  from './dialogs/dialogs.vue'

export default {
  name: 'Admin',
  components: {
    dialogs
  },
  data (){
    return {
      isCollapse: false,
      asideWidth: '150px',
      username: JSON.parse(sessionStorage.getItem('user')).first_name,
      dialogVisible: false,
      dialogReqData: null
    }
  },
  computed: {
    //面包屑格式胡
    filterBreadcrumb (){
      const breadcrumb = [];
      this.$route.matched.forEach(function(e,index) {
        if(e.meta.title && index){
          breadcrumb.push(e)
        }
      });
      return breadcrumb
    },
    //获取导航栏
    navList(){
      const role = this.$store.state.role;
      const navArr = mgtRouter.children;
      const newNavArr = [];
      navArr.forEach(e => {
        const roleArr = e.meta.role;
        if(roleArr?(roleArr.indexOf(role)>-1?true:false):true){
          let item = {};
          item.icon = e.meta.icon;
          item.title = e.meta.title;
          item.index = mgtRouter.path + '/' + (e.path=='/'?'':e.path+'/');
          newNavArr.push(item)
        }
      })
      return newNavArr
    },
  },
  methods: {
    //下拉
    handleCommand(command) {
      this.dialogReqData = command;
      this.dialogVisible = true
    },
    //跳转
    handleJump: handleJump,
    //导航栏隐藏
    collapse(key) {
      console.log(key);
      if(key){
        this.asideWidth = '65px'
      }else{
        this.asideWidth = '150px'
      }
        console.log(this.asideWidth)
    }
  }
}
</script>

<style scoped lang="scss">

  .header{
    position: relative;
    color: white;
    background-color: #443EFA;
    .logo{
      display: inline-block;
      vertical-align: middle;
    
    }
    h1{
      display: inline-block;
      margin: 0 0 0 10px;
      font-size: 1.25rem;
      line-height: 60px;
      vertical-align: middle;
    }
    .header-user{
      cursor: pointer;
      float: right;
      margin-right: .5rem;
      line-height: 60px;
      .el-dropdown{
        font-size: 1rem;
        color: white;
      }
    }
    .header-back-btn{
      float: right;
      margin-top: 1rem;
    }
  }
  .aside,
  .main{
    height: calc(100vh - 60px);
  }
</style>
