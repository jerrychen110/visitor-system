<template>
  <el-form-item
    :label="resData.set.label"
    :prop="resData.set.name"
    :rules="[{ required: resData.set.required, message: '请选择'+this.resData.set.label, trigger: 'blur' }]">
    <el-select
      v-model="resData.value"
      :placeholder="'请选择'+resData.set.label"
      class="w-100"
      @change="$emit('resData',resData)"
      :multiple=resData.set.multiple
      filterable clearable>
      <el-option :label="item[resData.set.optionLabel]" :value="item.id" v-for="item in listData" :key="item.id">
        <span style="float: left">{{ item[resData.set.optionLabel] }}</span>
        <i v-if="resData.set.deleteBtn" class="el-icon-circle-close delete-btn"  @click="deleteItem(item.id)"></i>
      </el-option>
    </el-select>
    <i v-if="resData.set.addBtn" class="el-icon-circle-plus form-item-btn" @click="addItem()"></i>
  </el-form-item>
</template>

<script>
export default {
  name: 'SelectList',
  props: ['data'],
  data (){
    return {
      // resData: this.data,
      listData: null
    }
  },
  created (){
    this.getList();
  },
  computed: {
    resData (){
      let data = this.data;
      data.set.addBtn = this.data.set.addBtn==false?false:true;
      data.set.deleteBtn = this.data.set.deleteBtn==false?false:true;
      data.set.optionLabel = this.data.set.optionLabel?this.data.set.optionLabel:'type_name';
      data.set.required = this.data.set.required==false?false:true;
      data.set.multiple = this.data.set.multiple==true?true:false;
      return data
    }
  },
  methods: {
    //获取列表
    getList() {
      let _this = this;
      axios({
        url: _this.resData.set.apiUrl,
        method: 'get',
        // withCredentials: true
      }).then(function (response) {
        // console.log(response);
        _this.listData = response.data.results;
      })
    },
    //新增
    addItem() {
      let _this = this;
      _this.$prompt('请输入'+_this.resData.set.label+'名称', '新建'+_this.resData.set.label, {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        // inputPattern: /[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?/,
        // inputErrorMessage: '邮箱格式不正确'
      }).then(({ value }) => {
        axios.post(_this.resData.set.apiUrl, {
          'type_name': value
        }).then(function (res) {
          // console.log(res.data.id);
          _this.getList();
          _this.resData.value = res.data.id;
        })
      }).catch(() => {});
    },
    //删除
    deleteItem(id) {
      let _this = this;
      _this.$confirm('此操作将用久删除该'+_this.resData.set.label+', 是否继续?', '删除'+_this.resData.set.label, {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        center: true
      }).then(() => {
        axios.delete(_this.resData.set.apiUrl+id+'/').then(function (response) {
          _this.getList();
          _this.resData.value = null;
        })
      }).catch(() => {});
    }
  }
}
</script>

<style scoped lang="scss">
.delete-btn{
  float: right; color: #8492a6; font-size: 1.25em; line-height: 34px;
}
</style>