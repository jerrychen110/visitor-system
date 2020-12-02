<template>
  <el-row>
    <el-col :span="16">
      <el-form ref="form" :model="form" label-width="80px" class="demo-ruleForm">
        <el-form-item label="用户名" prop="username" :rules="[{ required: true, message: '请输入用户名', trigger: 'blur' }]">
          <el-input v-model="form.username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="用户姓名" prop="firstname" :rules="[{ required: true, message: '请输入用户姓名', trigger: 'blur' }]">
          <el-input v-model="form.firstname" placeholder="请输入用户姓名"></el-input>
        </el-form-item>
        <!--<UploadFile-->
          <!--:data="{value: form.avatar, set: componentsSet.avatar}"-->
          <!--v-on:resData="resUploadFile">-->
        <!--</UploadFile>-->
        <el-form-item label="用户邮箱">
          <el-input v-model="form.email" placeholder="请输入用户邮箱"></el-input>
        </el-form-item>
        <!--<el-form-item label="用户年龄" prop="age" :rules="[{ required: true, message: '请输入用户年龄', trigger: 'blur' }]">-->
          <!--<el-input v-model="form.age" placeholder="请输入用户年龄"></el-input>-->
        <!--</el-form-item>-->
        <!--<el-form-item label="用户性别" prop="gender" :rules="[{ required: true, message: '请输入用户性别', trigger: 'blur' }]">-->
          <!--<el-radio-group v-model="form.gender">-->
            <!--<el-radio :label="1">男</el-radio>-->
            <!--<el-radio :label="2">女</el-radio>-->
          <!--</el-radio-group>-->
        <!--</el-form-item>-->
        <el-form-item label="用户状态">
          <el-checkbox v-model="form.is_active">是否激活用户</el-checkbox>
          <el-checkbox v-model="form.is_staff">是否管理员</el-checkbox>
          <el-checkbox v-model="form.is_superuser">是否超级管理员</el-checkbox>
        </el-form-item>
        <el-form-item label="用户描述">
          <el-input type="textarea" rows="5" v-model="form.description" placeholder="请输入用户描述"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit('form')">{{ pageType?'确定编辑':'立即创建' }}</el-button>
          <el-button @click="$router.back(-1)">取消</el-button>
        </el-form-item>
      </el-form>
    </el-col>
  </el-row>
</template>

<script>
import UploadFile from '@/components/UploadFile.vue'

export default {
  name: 'Creat',
  components: {
    UploadFile
  },
  data (){
    return {
      pageType: false,
      form: {
        username: '',
        firstname: '',
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
      },
      componentsSet: {
        avatar: {
          name: 'avatar',
          label: '用户头像',
          accept: '.jpg,.png',
          required: false
        }
      }
    }
  },
  created (){
    if(this.$route.params.id){
      this.getData();
      this.pageType = true;
    }
  },
  methods: {
    //获取数据
    getData(){
      let _this = this;
      axios.get('/API/base-api/user-profile/'+_this.$route.params.id+'/').then( res => {
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
          // if(!_this.pageType&&_this.form.avatar.length>0){
          //   fd.append('avatar', _this.form.avatar[0].raw, _this.form.avatar[0].name);
          // }
          fd.append('avatar', _this.form.avatar);
          fd.append('username', _this.form.username);
          fd.append('firstname', _this.form.firstname);
          fd.append('last_name', _this.form.last_name);
          fd.append('password', _this.pageType?_this.form.password:'pbkdf2_sha256$120000$7IpGiFgxgOmu$qkTGA80T9jw/3x3MlVHLxUCyoq+K6TG9/pl6uMFZBc4=');//默认密码
          fd.append('email', _this.form.email);
          fd.append('gender', _this.form.gender);
          fd.append('age', _this.form.age);
          fd.append('description', _this.form.description);
          fd.append('is_staff', _this.form.is_staff);
          fd.append('is_active', _this.form.is_active);
          fd.append('is_superuser', _this.form.is_superuser);
          // 接口
          axios({
            url: '/API/base-api/user-profile/' + (_this.pageType?_this.form.id+'/':''),
            data: fd,
            method: _this.pageType?'put':'post'
          }).then( res => {
            _this.$router.back(-1)
          })
        } else {
          return false;
        }
      });
    }
  }
}
</script>
