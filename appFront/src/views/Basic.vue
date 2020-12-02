<template>
  <div class="bg flex-center">
    <div class="basic-list">
      <el-carousel trigger="click"
        :autoplay="false"
        arrow="never"
        ref="carousel">
        <el-carousel-item v-for="itemList in basicList" :key="itemList.id">
          <el-card>
            <div slot="header" class="clearfix">
              <span>{{ itemList.name }}</span>
            </div>
            <el-row :gutter="40">
              <el-col :span="8" v-for="item in itemList.data" :key="item.id">
                <div class="basic-list__item" @click="itemClick(item)">
                  {{ item.name }}
                </div>
              </el-col>  
            </el-row>
          </el-card>
        </el-carousel-item>
      </el-carousel>
      
      <button class="carousel-btn" @click="setActiveItem('prev')"></button>
      <button class="carousel-btn carousel-btn-right" @click="setActiveItem('next')"></button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Basic',
  data (){
    return {
      basicList : [
        {
          'name': '图片识别',
          'data': [
            {
            'name': '人脸检测',
            'url': '/html5/FD'
            },{
            'name': '表情识别',
            'url': ''
            },{
            'name': '人脸对比对',
            'url': ''
            },{
            'name': '人脸特征点检测',
            'url': ''
            },{
            'name': '人脸聚类',
            'url': ''
            },{
            'name': '换脸',
            'url': ''
            },{
            'name': '颜色识别',
            'url': ''
            }
          ]
        },
        {
          'name': '视频识别',
          'data': [
            {
            'name': '打开视频',
            'url': ''
            },
            {
            'name': '人脸检测',
            'url': ''
            },
            {
            'name': '人脸识别',
            'url': ''
            },
            {
            'name': '人脸特征点检测',
            'url': ''
            },
            {
            'name': '表情识别',
            'url': ''
            },
            {
            'name': '物体移动检测',
            'url': ''
            },
            {
            'name': 'ROI跟踪检查',
            'url': ''
            }
          ]
        },
        {
          'name': '基于深度神经网络',
          'data': [
            {
            'name': '人脸检测(5点定位)',
            'url': ''
            },
            {
            'name': '人脸检测(68点定位)',
            'url': ''
            },
            {
            'name': '图像物体识别(GoogleNet)',
            'url': ''
            },
            {
            'name': '图像物体识别(MobileNet)',
            'url': ''
            },
            {
            'name': '视频物体识别(MobileNet)',
            'url': ''
            }
          ]
        },
        {
          'name': '自然语言',
          'data': [
            {
            'name': '打开小智语音助手',
            'url': ''
            }
          ]
        }
      ]
    }
  },
  methods: {
    setActiveItem(type) {
      if(type == 'prev'){
        this.$refs.carousel.prev()
      }else if(type == 'next'){
        this.$refs.carousel.next()
      }
    },
    itemClick(item) {
      const _this = this;
      if(item.url.length){
        window.open('http://127.0.0.1:9000/' + item.url);
      }else{
        _this.$message({
          type: 'warning',
          message: '敬亲期待!',
          duration: 2000
        });
      }
    }
  }
}
</script>

<style scoped lang="scss">
.carousel-btn{
  cursor: pointer;
  position: absolute;
  top: calc(50% - 2.5rem);
  left: -4rem;
  width: 3rem;
  height: 3rem;
  background-image: url("../assets/basic-left.png");
  background-color: transparent;
  background-size: 100% 100%;
  border: 0;
}
.carousel-btn-right{
  background-image: url("../assets/basic-right.png");
  left: auto;
  right: -4rem;
}
.basic-list{
  .basic-list__item{
    cursor: pointer;
    display: block;
    margin-bottom: 40px;
    padding: 1em 0;
    text-align: center;
    background-color: #0060fd;
    border: 2px solid #d9d9d9;
    box-shadow: 0 0 0 4px #4d4d57;
  }
}
</style>

<style lang="scss">
.basic-list{
  box-sizing: border-box;
  position: relative;
  padding-top: 5%;
  width: 80%;
  height: 100%;
  .el-carousel,
  .el-carousel__container{
    height: 90%;
  }
  .el-card{
    height: calc(100% - 4px);
    color: white;
    background-color: #2b2b37;
    border: 0;
  }
  .el-card__header{
    text-align: center;
    background-color: #23232f;
    border-bottom: 0;
  }
  .el-card__body{
    box-sizing: border-box;
    padding: 40px 40px 0 40px;
    height: calc(100% - 36px - 1em);
    overflow-x: auto;
  }
}
</style>
