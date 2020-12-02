<template>
  <el-row>
    <el-col :md="24" :lg="16" style="padding-right: 2.4rem;">
      <el-form ref="form" :model="form" label-width="80px">
        <SelectList
          :data="{value: form.patient_id, set: componentsSet.patient}"
          v-on:resData="resSelectList">
        </SelectList>
        <UploadFile
          :data="{value: form.voice_file, set: componentsSet.voice_file}"
          v-on:resData="resUploadFile">
        </UploadFile>
        <el-form-item label="语音文本">
          <div class="el-ql-editor ql-height-350">
            <vue-editor v-model="form.voice_text" :editorOptions="editorSettings"></vue-editor>
          </div>
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
import SelectList from '@/components/SelectList.vue'
import UploadFile from '@/components/UploadFile.vue'
import { VueEditor } from 'vue2-editor'

// 工具栏配置
const customToolbar = [
  ["bold", "italic", "underline", "strike"], // 加粗 斜体 下划线 删除线
  ["blockquote", "code-block"], // 引用  代码块
  [{ header: 1 }, { header: 2 }], // 1、2 级标题
  [{ list: "ordered" }, { list: "bullet" }], // 有序、无序列表
  [{ script: "sub" }, { script: "super" }], // 上标/下标
  [{ indent: "-1" }, { indent: "+1" }], // 缩进
  // [{'direction': 'rtl'}],                         // 文本方向
  [{ size: ["small", false, "large", "huge"] }], // 字体大小
  [{ header: [1, 2, 3, 4, 5, 6, false] }], // 标题
  [{ color: [] }, { background: [] }], // 字体颜色、字体背景颜色
  // [{ font: [] }], // 字体种类
  [{ align: [] }], // 对齐方式
  ["clean"], // 清除文本格式
  ["link", "image", "video"] // 链接、图片、视频
];

export default {
  name: 'Creat',
  components: {
    SelectList,
    UploadFile,
    VueEditor
  },
  data (){
    return {
      userData: JSON.parse(sessionStorage.getItem('user')),
      pageType: false,
      form: {
        patient_id: '',
        //voice_name: '',
        voice_file: [],
        voice_text: ''
      },
      componentsSet: {
        patient: {
          name: 'patient_id',
          label: '病人名称',
          apiUrl: '/API/base-api/api-patient/'+JSON.parse(sessionStorage.getItem('user')).id,
          optionLabel: 'patient_name',
          required: true
        },
        voice_file: {
          name: 'voice_file',
          label: '语音文件',
          accept: '.wav,*.pcm'
        }
      },
      editorSettings: {
        modules: {
          toolbar: customToolbar
        },
        placeholder: '请输入接口说明'
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
      axios.get('/API/base-api/voice/'+_this.$route.params.id+'/').then( res => {
        let data = res.data;
        if(data.voice_file){
          data.voice_file = [{name: data.voice_file.substring(data.voice_file.lastIndexOf("/")+1)}];
        }else{
          data.voice_file = [];
        }
        _this.form = data;
        if(data.user_id){
            _this.userId = data.user_id;
        }else{
            _this.userId = data.user;
        }
      })
    },
    //select组件赋值
    resSelectList(res) {
      this.form[res.set.name] = res.value;
      this.$refs['form'].clearValidate([res.set.name]);
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
          fd.append('patient_id', _this.form.patient_id?_this.form.patient_id:[]);

          if(_this.isChina(_this.form.voice_file[0].name)){
              _this.$message({message: '上传的文件名中不能包含中文！', type: 'error'});
              return false;
          }
          if(_this.form.voice_file[0].name.indexOf(" ") > 0){
              _this.$message({message: '上传的文件名中不能包含空格！', type: 'error'});
              return false;
          }
          if(_this.form.voice_file[0].raw!=undefined){
              fd.append('voice_file', _this.form.voice_file[0].raw, _this.form.voice_file[0].name);
          }else{
              fd.append('voice_file', _this.form.voice_file[0].name);
          }
          fd.append('voice_text', _this.form.voice_text);
          
          let userId = _this.userData.id;
          if(_this.pageType){
              fd.append('id', _this.form.id);
              userId = _this.userId;
          }
          fd.append('user_id', userId);
          // 接口
          axios({
            url: '/API/base-api/voice/' + (_this.pageType?_this.form.id+'/':''),
            data: fd,
            method: _this.pageType?'put':'post'
          }).then( res => {
              if(res.data.results==100){
                _this.$message({message: '语音名称已经存在，请修改名称后再创建！', type: 'error'});
                return false;
              }else if(res.data.results==300){
                _this.$message({message: '上传的语音文件已经存在，请修改名称后再传！', type: 'error'});
                return false;
              }else{
                  _this.$router.back(-1);
              }
          })
        } else {
          return false;
        }
      });
    },
    isChina(s){
      var patrn=/[\u4E00-\u9FA5]|[\uFE30-\uFFA0]/gi;
      if(!patrn.exec(s)){
        return false;
      }else{
        return true;
      }
    }
  }
}
</script>
