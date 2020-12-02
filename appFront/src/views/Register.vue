<template>
  <div class="bg login-bg flex-center">
    <div class="login-card">
      <el-card>
        <div slot="header" class="text-center">
          <span>用户注册</span>
        </div>
        <el-form ref="form" :model="form" :rules="rules" :hide-required-asterisk="true" label-width="80px">
          <el-form-item label="登录账号" prop="username">
            <el-input
              v-model="form.username"
              placeholder="请输入登录账号"
              @keyup.enter.native="register('form')">
            </el-input>
          </el-form-item>
          <el-form-item label="用户姓名" prop="first_name">
            <el-input
              v-model="form.first_name"
              placeholder="请输入用户姓名"
              @keyup.enter.native="register('form')">
            </el-input>
          </el-form-item>
          <el-form-item label="登录密码" prop="password">
            <el-input
              show-password
              type="password"
              v-model="form.password"
              placeholder="请输入登录密码"
              @keyup.enter.native="register('form')">
            </el-input>
          </el-form-item>
          <el-form-item label="确认密码" prop="password2">
            <el-input
              show-password
              type="password"
              v-model="form.password2"
              placeholder="请再次输入登录密码"
              @keyup.enter.native="register('form')">
            </el-input>
          </el-form-item>
          <div>
            <el-button type="primary" class="w-100" @click="register('form')">注册</el-button>
            <div class="mtm text-right">
              <small class="text-muted mrs">已有账户，请点击</small>
              <router-link to='login'>
                <el-button type="warning" size="mini">登录</el-button>
              </router-link>
            </div>
          </div>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data (){
    let pass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'));
      } else if (value !== this.form.password) {
        callback(new Error('两次输入密码不一致!'));
      } else {
        callback();
      }
    };
    return {
      form: {
        username: '',
        password: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入登录账号', trigger: 'blur' }
        ],
        first_name: [
          { required: true, message: '请输入用户姓名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入登录密码', trigger: 'blur' },
          { pattern: /^[a-zA-Z0-9]{4,16}$/, message: '4到16位（字母，数字）' }
        ],
        password2: [
          { validator: pass2, trigger: 'blur' }
        ]
      }
    };
  },
  methods: {
    register(formName) {  //用户名注册
      const _this = this;
      _this.$refs[formName].validate((valid) => {
        if (valid) {
          axios.post('/API/register/', {
            'username': _this.form.username,
            'first_name': _this.form.first_name,
            'password': _this.form.password
          }).then(function (res) {
            if (res.data.code == 200){
              _this.$router.push({path:'/login'})
            }else{
              _this.$message({message: '用户名已经存在，请重新修改用户名！', type: 'error'});
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
