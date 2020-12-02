<template>
  <header class="header">
    <!-- <div class="header-left">
      <el-col :span="11" class="h-100">
        <div class="index-jqr">
          <img class="logo" src="@/assets/logo.png" alt />
        </div>
      </el-col>
    </div> -->
    <h2 class="index-title">随访系统</h2>
    <div class="header-right">
      <span class="mrm">{{ username }}</span>
      <!--<button class="button mrm" style="cursor:pointer" @click="getIp()">服务地址</button>-->
      <router-link class="button mrm" to="/mgt/">管理</router-link>
      <button class="button" style="cursor:pointer" @click="logout()">注销</button>
    </div>
   
  </header>
</template>

<script>
export default {
  name: "Header",
  props: {
    title: String,
  },
  data() {
    return {
      username: JSON.parse(sessionStorage.getItem("user")).first_name,
    };
  },
  methods: {
    getIp() {
      let _this = this;
      axios({
        url: "/API/local-area-ip/",
      }).then(function (response) {
        console.log(response);
        if (response.status == 200 && response.data.error_code == 200) {
          _this.$alert("IP：" + response.data.ip_address, "内网IP", {
            confirmButtonText: "确定",
            callback() {},
          });
          return;
        } else {
          _this.$message({
            type: "warning",
            message: "获取地址失败！",
            duration: 2000,
          });
        }
      });
    },
    logout() {
      const _this = this;
      _this
        .$confirm("确定要注销账户吗?", "注销", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
          center: true,
        })
        .then(() => {
          axios({
            url: "/API/logout/",
            method: "post",
            headers: { "Hide-Message": true },
          }).then(function (res) {
            _this.$store.commit("setIsLogin", false);
            _this.$router.push({ path: "/login" });
            localStorage.removeItem("UserData");
          });
        })
        .catch(() => {});
    },
    hide() {
      let type = true;
      const pageName = this.$route.name;
      const hidePages = ["Home"];
      hidePages.forEach(function (item, index) {
        if (item == pageName) {
          type = false;
        }
      });
      return type;
    },
  },
};
</script>

<style scoped lang="scss">
.header {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1;
  width: 100%;
  height: 4rem;
  color: white;
  .title {
    margin-top: 0;
    margin-bottom: 0;
    width: 100%;
    font-size: 1rem;
    text-align: center;
    line-height: 4rem;
  }
  .header-left {
    position: absolute;
    top: 0;
    left: 0;
    display: inline-block;
    padding-left: 1.5rem;
    line-height: 5.5rem;
    .button {
      padding: 0.25em 1.5em;
      font-size: 0.875em;
      color: white;
      text-decoration: none;
      background-color: transparent;
      border: 1px solid white;
      border-radius: 0.25rem;
    }
  }
  .header-right {
    position: absolute;
    top: 0;
    right: 0;
    display: inline-block;
    padding: 1.125rem 1.5em;
    .button {
      padding: 0.25em 1.5em;
      font-size: 0.875em;
      color: white;
      text-decoration: none;
      background-color: transparent;
      border: 1px solid white;
      border-radius: 0.25rem;
    }
  }
  .index-title {
    position: absolute;
    top: 0;
    width: 100%;
    color: white;
    text-align: center;
  }
 
}
</style>
