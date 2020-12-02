<template>
  <div>
    <el-row>
      <el-col :span="12">
        <el-input placeholder="请输入内容" v-model="query" class="input-with-select">
          <el-button slot="append" icon="el-icon-search" @click="getList()"></el-button>
        </el-input>
      </el-col>
      <el-col :span="12" style="text-align: right">
        <router-link to="creat" tag="span">
          <el-button type="primary" icon="el-icon-plus">新建语音</el-button>
        </router-link>
      </el-col>
      <el-col :span="24">
        <el-table
          :data="tableData"
          style="width: 100%;margin-bottom: 20px;">
          <el-table-column
            :prop="item.prop"
            :label="item.label"
            :min-width="item.width"
            :show-overflow-tooltip="true"
            v-for="item in theader" :key="item.id">
          </el-table-column>
          <el-table-column
            prop="created"
            label="创建时间"
            :formatter="createdFormat"
            width="180">
          </el-table-column>
          <el-table-column
            fixed="right"
            label="操作"
            width="200">
            <template slot-scope="scope">
              <el-button-group>
                <el-button size="mini" @click="handleJump('doc/',scope.row.id)">文档</el-button>
                <el-button size="mini" type="primary" @click="handleJump('editor/',scope.row.id)" >编辑</el-button>
                <el-button size="mini" type="danger"  @click="handleDelete(scope.$index, scope.row)">删除</el-button>
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
      <el-col :span="12" style="text-align: right">
        <el-pagination
          background
          layout="prev, pager, next"
          @current-change="currentChange"
          :page-size="this.pageSize"
          :current-page="this.currentPage"
          :total="this.count">
        </el-pagination>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import  { createdFormat, publicFormat, handleJump }  from '@/plugins/components.js'

export default {
  name: 'List',
  data (){
    return {
      userData: JSON.parse(sessionStorage.getItem('user')),
      query: null,
      pageSize: 8,
      currentPage: 1,
      count: null,
      tableData: null,
      theader: [{
        prop: 'id',
        label: 'ID',
        width: '8%'
      },{
        prop: 'voice_name',
        label: '名称',
        width: '15%'
      },{
        prop: 'voice_text',
        label: '语音文本',
        width: '25%'
      },{
        prop: 'patient_name',
        label: '病人姓名',
        width: '20%'
      },{
        prop: 'username',
        label: '创建者',
        width: '15%'
      }]
    }
  },
  created (){
    this.getList();
  },
  methods: {
    //时间格式化
    createdFormat: createdFormat,
    //状态格式化
    publicFormat: publicFormat,
    //跳转
    handleJump: handleJump,
    //获取列表
    getList (){
      let _this = this;
      axios({
        url: '/API/base-api/query-voice/',
        params: {
          page: _this.currentPage,
          voice_text: _this.query,
          user_id: _this.userData.id
        }
      }).then(function (response) {
        _this.tableData = response.data.results;
        _this.count = response.data.total;
      })
    },
    //翻页
    currentChange (val){
      this.currentPage = val;
      this.getList();
    },
    //删除
    handleDelete (index, row){
      let _this = this;
      _this.$confirm('此操作将永久删除该文件, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        center: true
      }).then(() => {
        axios.delete('/API/base-api/voice/'+row.id+'/').then(function (response) {
          _this.getList();
        })
      }).catch(() => {});
    }
  }
}
</script>
