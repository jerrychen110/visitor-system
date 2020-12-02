<template>
    <el-row>
        <el-col :span="24">
          <el-form ref="form" :model="form" label-width="80px" class="demo-ruleForm">
            <el-form-item label="用户名">
              <el-input v-model="form.username" disabled="disabled"></el-input>
            </el-form-item>
            <el-form-item label="原密码" prop="oldPassword" :rules="[{ required: true, message: '请输入原密码', trigger: 'blur' }]">
              <el-input v-model="form.oldPassword" placeholder="请输入原密码"></el-input>
            </el-form-item>
            <el-form-item label="新密码" prop="newPassword" :rules="[{ required: true, message: '请输入新密码', trigger: 'blur' }]">
              <el-input :type="show.new?'text':'password'" v-model="form.newPassword" placeholder="请输入新密码"></el-input>
            </el-form-item>
            <el-form-item label="确认密码" prop="verifyNewPassword" :rules="[{ required: true, message: '请再次输入新密码', trigger: 'blur' }]">
              <el-input :type="show.check?'text':'password'" v-model="form.verifyNewPassword" placeholder="请再次输入新密码"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="onSubmit('form')">修改</el-button>
            </el-form-item>
          </el-form>
        </el-col>
    </el-row>
</template>

<script>
    export default {
        name: "Password",
        data (){
            return {
              form: {
                username: '',
                oldPassword: null,
                newPassword: null,
                verifyNewPassword: null
              },
              show: {
                  old: false,
                  new: false,
                  check: false
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
                let data = res.data;
                _this.form.id = data.id;
                _this.form.username = data.username;
              })
            },
            onSubmit(formName) {
                let _this = this;
                _this.$refs[formName].validate((valid) => {
                    if(valid){
                      if(_this.form.newPassword!=_this.form.verifyNewPassword){
                          _this.$message({message: '新密码与确认密码不一致！', type: 'error'});
                          return false;
                      }
                      //数据
                      let fd = new FormData();
                      fd.append('username', _this.form.username);
                      fd.append('oldPassword', _this.form.oldPassword);
                      fd.append('newPassword', _this.form.newPassword);
                      // 接口
                      axios({
                        url: '/API/base-api/user-profile/' + _this.form.id + '/change-password',
                        data: fd,
                        method: 'put'
                      }).then( res => {
                          console.log(res);
                          if(res.data.results==300){
                            _this.$message({message: '原密码错误！', type: 'error'});
                            return false;
                          }else if(res.data.results==200) {
                            _this.$message({message: '修改成功！', type: 'success'});
                          }
                      })
                    }else{
                        if(_this.form.oldPassword==null||_this.form.oldPassword==''){
                            _this.$message({message: '原密码必填！', type: 'error'});
                            return false;
                        }
                        if(_this.form.newPassword==null||_this.form.newPassword==''){
                            _this.$message({message: '新密码必填！', type: 'error'});
                            return false;
                        }
                        if(_this.form.verifyNewPassword==null||_this.form.verifyNewPassword==''){
                            _this.$message({message: '确认密码必填！', type: 'error'});
                            return false;
                        }
                    }
                });
            }
        }
    }
</script>