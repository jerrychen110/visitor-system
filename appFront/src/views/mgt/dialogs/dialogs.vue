<template>
  <div>
    <el-dialog
      :title="name"
      :visible.sync="visible"
      @close="$emit('update:show', false)"
      :show="show">
      <div :is="url"></div>
    </el-dialog>
  </div>
</template>
 
<script>
import  Password  from './Password.vue'
import  UserInfo  from './UserInfo.vue'

export default {
  data () {
    return {
      visible: this.show,
      name: null,
      url: null
    };
  },
  props: {
    show: {
      type: Boolean,
      default: false
    },
    reqData: Object
  },
  components: {
    Password,
    UserInfo,
  },
  watch: {
    reqData(val) {
      this.url = val.url;
      this.name = val.name;
    },
    show () {
      this.visible = this.show;
    }
  }
};
</script>