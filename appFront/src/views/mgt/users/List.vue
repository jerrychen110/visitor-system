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
          <el-button type="primary" icon="el-icon-plus">新建用户</el-button>
        </router-link>
      </el-col>
      <el-col :span="24">
        <el-table
          :data="tableData"
          style="width: 100%;margin-bottom: 20px;">
          <!--<el-table-column-->
            <!--type="selection"-->
            <!--width="50">-->
          <!--</el-table-column>-->
          <el-table-column
            :prop="item.prop"
            :label="item.label"
            :show-overflow-tooltip="true"
            v-for="item in theader" :key="item.id">
          </el-table-column>
          <el-table-column
            label="角色">
            <template slot-scope="scope">
              {{ scope.row.is_superuser?'超级管理员':(scope.row.is_staff?'管理员':'用户') }}
            </template>
          </el-table-column>
          <el-table-column
            label="状态"
            width="50">
            <template slot-scope="scope">
              <i :class="scope.row.is_active?'el-icon-success el-link el-link--success':'el-icon-error el-link el-link--danger' "></i>
            </template>
          </el-table-column>
          <el-table-column
            prop="last_login"
            label="最后登陆时间"
            :formatter="createdFormat"
            width="180">
          </el-table-column>
          <el-table-column
            fixed="right"
            width="200"
            label="操作">
            <template slot-scope="scope">
              <el-button-group>
                <el-button size="mini" @click="handleJump('editor/',scope.row.id)">编辑</el-button>
                <el-button size="mini" type="primary" @click="restorePassword(scope.row)">重置</el-button>
                <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
      <!--<el-col :span="12">-->
        <!--<el-button type="danger" size="small" icon="el-icon-delete">批量删除</el-button>-->
      <!--</el-col>-->
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
import  { createdFormat, handleJump }  from '@/plugins/components.js'

export default {
  name: 'List',
  data (){
    return {
      query: null,
      pageSize: 8,
      currentPage: 1,
      count: null,
      tableData: null,
      theader: [{
        prop: 'id',
        label: '用户ID'
      },{
        prop: 'username',
        label: '登录账号'
      },{
        prop: 'firstname',
        label: '用户姓名'
      },{
        prop: 'email',
        label: '用户邮箱'
      }]
    }
  },
  created (){
    this.getList();
  },
  methods: {
    //时间格式化
    createdFormat: createdFormat,
    //跳转
    handleJump: handleJump,
    //获取列表
    getList (){
      let _this = this;
      axios({
        url: '/API/base-api/query-user-profile/',
        params: {
          page: _this.currentPage,
          username: _this.query
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
        axios.delete('/API/base-api/user-profile/'+row.id+'/').then(function (response) {
          _this.getList();
        })
      }).catch(() => {});
    },
    restorePassword(row){
        let _this = this;
      _this.$confirm('确定要重置密码吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        center: true
      }).then(() => {
        axios.put('/API/base-api/user-profile/'+row.id+'/restore-password').then(function (response) {
          _this.$message({message: '密码重置成功！', type: 'success'});
          _this.getList();
        })
      }).catch(() => {});
    }
  }
}
</script>