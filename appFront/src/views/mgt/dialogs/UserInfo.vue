<template>
  <el-row>
    <el-col :span="24">
      <el-form ref="form" :model="form" label-width="80px" class="demo-ruleForm">
        <el-form-item label="用户名">
          <el-input v-model="form.username" disabled="disabled"></el-input>
        </el-form-item>
        <el-form-item label="用户姓名" prop="first_name" :rules="[{ required: true, message: '请输入用户姓名', trigger: 'blur' }]">
          <el-input v-model="form.first_name" placeholder="请输入用户姓名"></el-input>
        </el-form-item>
        <el-form-item label="用户性别" prop="gender" :rules="[{ required: true, message: '请输入用户性别', trigger: 'blur' }]">
          <el-radio-group v-model="form.gender">
            <el-radio :label="1">男</el-radio>
            <el-radio :label="2">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="用户邮箱">
          <el-input v-model="form.email" placeholder="请输入用户邮箱"></el-input>
        </el-form-item>
        <el-form-item label="用户描述">
          <el-input type="textarea" rows="5" v-model="form.description" placeholder="请输入用户描述"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit('form')">保存</el-button>
        </el-form-item>
      </el-form>
    </el-col>
  </el-row>
</template>

<script>
export default {
  name: 'UserInfo',
  data (){
    return {
      form: {
        username: '',
        first_name: '',
        last_name: '',
        password: '',
        passwordAgain: '',
        email: '',
        avatar: [],
        gender: 1,
        age: 0,
        description: '',
        is_staff: 0,
        is_active: 1,
        is_superuser: 0
      }
    }
  },
  created (){
    if(sessionStorage.getItem('isLogin')){
        const userData = JSON.parse(sessionStorage.getItem('user'));
        if(userData.id){
          this.getData(userData.id);
        }
    }else{
        const _this = this;
        _this.$message({
          type: 'warning',
          message: '没有登录!',
          duration: 2000
        });
    }
  },
  methods: {
    //获取数据
    getData(id){
      let _this = this;
      axios.get('/API/base-api/user-profile/'+id+'/').then( res => {
        // console.log(res)
        let data = res.data;
        if(data.avatar){
          data.avatar = [{name: data.avatar.substring(data.avatar.lastIndexOf("/")+1)}];
        }else{
          data.avatar = [];
        }
        _this.form = data;
      })
    },
    //上传组件赋值
    resUploadFile(res) {
      this.form[res.set.name] = res.value;
      this.$refs['form'].clearValidate([res.set.name]);
    },
    //提交
    onSubmit(formName) {
      let _this = this;
      _this.$refs[formName].validate((valid) => {
        if (valid) {
          //数据
          let fd = new FormData();
          fd.append('username', _this.form.username);
          fd.append('first_name', _this.form.first_name);
          fd.append('last_name', _this.form.last_name);
          fd.append('password', _this.form.password);
          fd.append('email', _this.form.email);
          fd.append('gender', _this.form.gender);
          fd.append('age', _this.form.age);
          fd.append('description', _this.form.description);
          fd.append('is_staff', _this.form.is_staff);
          fd.append('is_active', _this.form.is_active);
          fd.append('is_superuser', _this.form.is_superuser);
          // 接口
          axios({
            url: '/API/base-api/user-profile/' + _this.form.id + '/',
            data: fd,
            method: 'put'
          }).then( res => {
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
