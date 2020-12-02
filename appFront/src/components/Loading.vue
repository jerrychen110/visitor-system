<template>
<div class="loading"></div>
</template>
<script>
export default {
  name: 'Loading' // 定义的组件名称 使用时写法：loading
}
</script>
 
<style scoped>
.loading {
  position: fixed;
  left: 50%;
  top: 30%;
  background: url('~@/assets/loading-bars.svg') center center no-repeat #2980B9;
  width: 10vw;
  height: 20vh;
  z-index: 1000;
}
</style>