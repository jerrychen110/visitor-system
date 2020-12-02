<template>
  <el-form-item :label="resData.set.label" :prop="resData.set.name" v-show="resData.set.show" :rules="[{ required: resData.set.required, message: '请选择'+resData.set.label, disabled:resData.set.disabled, trigger: 'blur' }]">
    <el-upload
      action="#"
      :file-list="resData.value"
      :auto-upload="false"
      :on-change="handleChange"
      :on-remove="handleRemove"
      :accept="resData.set.accept">
      <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
      <div slot="tip" class="el-upload__tip" v-if="resData.set.accept">只能上传{{ resData.set.accept }}文件</div>
    </el-upload>
  </el-form-item>
</template>

<script>
export default {
  name: 'UploadFile',
  props: ['data'],
  computed: {
    resData (){
      let data = this.data;
      data.set.required = this.data.set.required==false?false:true;
      data.set.show = this.data.set.show==false?false:true;
      return this.data
    }
  },
  methods: {
    //移除文件
    handleRemove(file, fileList) {
      this.resData.value = [];
      this.$emit('resData',this.resData);
    },
    //只上传一个文件
    handleChange(file, fileList) {
      this.resData.value = [file];
      this.$emit('resData',this.resData);
    }
  }
}
</script>