<template>
  <div>
    <el-row>
      <el-col :span="12">
        <el-input placeholder="请输入内容" v-model="query" class="input-with-select">
          <el-button slot="append" icon="el-icon-search" @click="getList()"></el-button>
        </el-input>
      </el-col>
      <el-col :span="12" style="text-align: right">
        <router-link to="/mgt/patients/creat" tag="span">
          <el-button type="primary" icon="el-icon-plus">录入病人信息</el-button>
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
            prop="patient_sex"
            label="性别"
            :formatter="patientSex"
            width="180">
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
                 <!-- <el-button size="mini" @click="handleJump2('/',scope.row.id)">会话</el-button> -->
                <el-button size="mini" type="primary" @click="handleJump('editor/',scope.row.id)" :disabled="userData.is_superuser!=true&&userData.is_staff!=true">编辑</el-button>
                <el-button
                  size="mini"
                  type="danger"
                  @click="handleDelete(scope.$index, scope.row)" :disabled="userData.is_superuser!=true&&userData.is_staff!=true">删除</el-button>
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
import  {patientSex, createdFormat, publicFormat, handleJump,handleJump2 }  from '@/plugins/components.js'

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
        width: '5%'
      },{
        prop: 'patient_name',
        label: '姓名',
        width: '15%'
      },{
        prop: 'patient_age',
        label: '年龄',
        width: '5%'
      },{
        prop: 'patient_address',
        label: '地址',
        width: '30%'
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
    //性别格式化
    patientSex: patientSex,
    //跳转
    handleJump: handleJump,
    handleJump2: handleJump2,
    //获取列表
    getList (){
      let _this = this;
      axios({
        url: '/API/base-api/query-patient/',
        params: {
          page: _this.currentPage,
          patient_name: _this.query,
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
        axios.delete('/API/base-api/patient/'+row.id+'/').then(function (response) {
          _this.getList();
        })
      }).catch(() => {});
    }
  }
}
</script>
