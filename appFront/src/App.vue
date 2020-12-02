<template>
  <div id="app">
    <Header title="" v-if="headShow()"/>
    <!-- router-view -->
    <router-view/>
    <!-- router-view -->
  </div>
</template>

<script>
import Header from './components/Header.vue'

export default {
  name: 'app',
  components: {
    Header
  },
  methods:{
    headShow () {
      let type = false;
      const pageName = this.$route.name;
      const hidePages = ['Home', 'Apps'];
      hidePages.forEach(function(item, index){
        if(item == pageName){
          type = true
        }
      })
      return type
    }
  }
}
</script>
<style lang="scss">
@import "@/assets/scss/space.scss";
@import "@/assets/scss/layout.scss";

body{
  margin: 0;
}
.bg{
  box-sizing: border-box;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  padding-top: 4rem;
  background-image: url("assets/bg.jpg");
   
  background-size: 100% 100%;
}
.login-bg{
  padding-top: 0;
  .login-card{
    width: 400px;
  }
}
a.el-button{
  text-decoration: none;
}
.form-item-btn{
  cursor: pointer;
  position: absolute;
  right: -3rem;
  font-size: 2.4rem;
  color: #2b89ed;
}

</style>
