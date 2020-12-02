<template>
  <div class="bg login-bg flex-center">
    <div class="login-card">
      <el-card>
        <div slot="header" class="text-center">
          <span>录入病人信息</span>
        </div>
      <el-form ref="form" :model="form" label-width="100px">
        <el-form-item label="姓名" prop="patient_name" :rules="[{ required: true, message: '请输入姓名', trigger: 'blur' }]">
          <el-input v-model="form.patient_name" placeholder="请输入姓名"></el-input>
        </el-form-item>
        <el-form-item label="性别">
          <el-radio-group v-model="form.patient_sex">
            <el-radio :label="false">男</el-radio>
            <el-radio :label="true">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="年龄" prop="patient_age" :rules="[{ required: true, message: '请输入年龄', trigger: 'blur' }]">
          <el-input v-model="form.patient_age" placeholder="请输入年龄"></el-input>
        </el-form-item>
        <el-form-item label="地址">
          <el-input v-model="form.patient_address" placeholder="请输入地址"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit('form')">{{ pageType?'确定编辑':'立即创建' }}</el-button>
          <el-button @click="$router.back(-1)">取消</el-button>
        </el-form-item>
      </el-form>
     </el-card>
    </div>
  </div>
</template>

<script>

export default {
  name: 'PatientInfo',
  data (){
    return {
      userData: JSON.parse(sessionStorage.getItem('user')),
      pageType: false,
      form: {
        patient_name: '',
        patient_sex: false,
        patient_age: '',
        patient_address: ''
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
      axios.get('/API/base-api/patient/'+_this.$route.params.id+'/').then( res => {
        let data = res.data;
        _this.form = data;
      })
    },
    //提交
    onSubmit(formName) {
      let _this = this;
      _this.$refs[formName].validate((valid) => {
        if (valid) {
          //数据
          let fd = new FormData();
          fd.append('patient_name', _this.form.patient_name);
          fd.append('patient_sex', _this.form.patient_sex);
          fd.append('patient_age', _this.form.patient_age);
          fd.append('patient_address', _this.form.patient_address);
          fd.append('user_id', _this.userData.id);
          // 接口
          axios({
            url: '/API/base-api/patient/' + (_this.pageType?_this.form.id+'/':''),
            data: fd,
            method: _this.pageType?'put':'post'
          }).then( res => {
           _this.$router.push({ path: "/" });
          })
        } else {
          return false;
        }
      });
    }
  }
}
</script>