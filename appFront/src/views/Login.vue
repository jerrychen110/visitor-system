<template>
  <div class="bg login-bg flex-center">
    <div class="login-card">
      <el-card>
        <div slot="header" class="text-center">
          <span>用户登录</span>
        </div>
        <el-form ref="form" :model="form" :rules="rules" :hide-required-asterisk="true" label-width="80px">
          <el-form-item label="登录账号" prop="username">
            <el-input
              v-model="form.username"
              placeholder="请输入登录账号"
              @keyup.enter.native="login('form')">
            </el-input>
          </el-form-item>
          <el-form-item label="登录密码" prop="password">
            <el-input
              show-password
              type="password"
              v-model="form.password"
              placeholder="请输入登录密码"
              @keyup.enter.native="login('form')">
            </el-input>
          </el-form-item>
          <div>
            <el-button type="primary" class="w-100" @click="login('form')">登录</el-button>
            <div class="mtm text-right">
              <small class="text-muted mrs">没有账户，请点击</small>
              <router-link to='register'>
                <el-button type="warning" size="mini">注册</el-button>
              </router-link>
            </div>
          </div>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script>
import  { getCookie }  from '@/plugins/components.js';

export default {
  name: 'Login',
  data (){
    return {
      form: {
        username: '',
        password: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入登录账号', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入登录密码', trigger: 'blur' },
          { pattern: /^[a-zA-Z0-9]{4,16}$/, message: '4到16位（字母，数字）' }
        ]
      }
    };
  },
  created (){
    this.initUserPass();
  },
  methods: {
    initUserPass(){
        const _this = this;
        if(localStorage.getItem("userName")&&localStorage.getItem("userPass")){
            _this.form.username = localStorage.getItem("userName");
            _this.form.password = localStorage.getItem("userPass");
        }
    },
    login(formName) {  //用户名登录
      const _this = this;
      _this.$refs[formName].validate((valid) => {
        debugger
        if (valid) {
          axios({
            url: '/API/normal-login/', 
            data: {
              'username': _this.form.username,
              'password': _this.form.password
            },
            method: 'post',
            headers: {'Hide-Message': true}
          }).then(function (res) {
            if(res.status == 200){
              debugger
                _this.$store.commit('setIsLogin', true);
                _this.$store.commit('setToken', getCookie('csrftoken'));
                _this.$store.commit('setRole', res.data.is_superuser?'超级管理员':(res.data.is_staff?'管理员':'用户'));
                _this.$store.commit('setUser', JSON.stringify(res.data));
                // localStorage.setItem('UserData', JSON.stringify(res.data))
                //保存用户名、密码到localStorage
                localStorage.setItem('userName', _this.form.username);
                localStorage.setItem('userPass', _this.form.password);
                _this.$message({
                  message: '登录成功！1秒后自动跳转至首页。',
                  type: 'success',
                  duration: 1000,
                  onClose: () => {
                    _this.$router.push({path:'/'})
                  }
                });
            }else if(res.data.code == 201) {
              _this.$message({
                type: 'error',
                message: '用户名或者密码错误!',
                duration: 2000
              })
            }
          })
        } else {
          return false;
        }
      })
    }
  }
}
</script>
