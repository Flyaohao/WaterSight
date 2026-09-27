<template>
  <div>

    <div class="operation">
      <el-button type="danger" plain @click="delBatch">批量删除</el-button>
    </div>

    <div class="table">
      <el-table :data="tableData" stripe  @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" align="center"></el-table-column>
        <el-table-column prop="id" label="序号" width="80" align="center" sortable></el-table-column>
        <el-table-column prop="activityId" label="活动ID" show-overflow-tooltip></el-table-column>
        <el-table-column prop="activityName" label="活动名称" show-overflow-tooltip></el-table-column>
        <el-table-column prop="userId" label="报名人ID" show-overflow-tooltip></el-table-column>
        <el-table-column prop="userName" label="报名人" show-overflow-tooltip></el-table-column>
        <el-table-column prop="time" label="报名时间"></el-table-column>

        <el-table-column label="操作" width="180" align="center">
          <template v-slot="scope">
            <el-button plain type="danger" size="mini" @click=del(scope.row.id)>删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div style="margin: 10px 0; display: flex; align-items: center;">
        <el-pagination
          background
          @current-change="handleCurrentChange"
          @size-change="handleSizeChange"
          :current-page.sync="pageNum"
          :page-size="pageSize"
          :page-sizes="[10, 20, 30, 50]"
          :pager-count="5"
          layout="total, sizes, prev, pager, next"
          :total="total">
        </el-pagination>
        <div class="jump-page">
          <span>前往</span>
          <el-input
            v-model.number="jumpPage"
            size="mini"
            style="width: 70px; margin: 0 5px;"
            @keyup.enter.native="handleJumpPage">
          </el-input>
          <span>页</span>
          <el-button size="mini" type="primary" @click="handleJumpPage" style="margin-left: 5px">跳转</el-button>
        </div>
      </div>
    </div>


  </div>
</template>

<script>
export default {
  name: "ActivitySign",
  data() {
    return {
      tableData: [],  // 所有的数据
      pageNum: 1,   // 当前的页码
      pageSize: 10,  // 每页显示的个数
      total: 0,
      user: JSON.parse(localStorage.getItem('xm-user') || '{}'),
      rules: {
      },
      ids: [],
      jumpPage: 1,
    }
  },
  created() {
    this.load(1)
  },
  methods: {
    del(id) {   // 单个删除
      this.$confirm('您确定删除吗？', '确认删除', {type: "warning"}).then(response => {
        this.$request.delete('/activitySign/delete/' + id).then(res => {
          if (res.code === '200') {   // 表示操作成功
            this.$message.success('操作成功')
            this.load(1)
          } else {
            this.$message.error(res.msg)  // 弹出错误的信息
          }
        })
      }).catch(() => {
      })
    },
    handleSelectionChange(rows) {   // 当前选中的所有的行数据
      this.ids = rows.map(v => v.id)   //  [1,2]
    },
    delBatch() {   // 批量删除
      if (!this.ids.length) {
        this.$message.warning('请选择数据')
        return
      }
      this.$confirm('您确定批量删除这些数据吗？', '确认删除', {type: "warning"}).then(response => {
        this.$request.delete('/activitySign/delete/batch', {data: this.ids}).then(res => {
          if (res.code === '200') {   // 表示操作成功
            this.$message.success('操作成功')
            this.load(1)
          } else {
            this.$message.error(res.msg)  // 弹出错误的信息
          }
        })
      }).catch(() => {
      })
    },
    load(pageNum) {  // 分页查询
      if (pageNum) this.pageNum = pageNum
      this.$request.get('/activitySign/selectPage', {
        params: {
          pageNum: this.pageNum,
          pageSize: this.pageSize,
        }
      }).then(res => {
        this.tableData = res.data?.list
        this.total = res.data?.total
      })
    },
    handleCurrentChange(pageNum) {
      this.load(pageNum)
    },
    handleSizeChange(pageSize) {
      this.pageSize = pageSize
      this.pageNum = 1  // 切换每页显示条数时，重置为第一页
      this.load()
    },
    handleJumpPage() {
      if (!this.jumpPage) {
        this.jumpPage = 1
        return
      }
      
      // 计算最大页数
      const maxPage = Math.ceil(this.total / this.pageSize)
      
      // 确保页码在有效范围内
      if (this.jumpPage < 1) {
        this.jumpPage = 1
      } else if (this.jumpPage > maxPage) {
        this.jumpPage = maxPage
      }
      
      if (this.pageNum !== this.jumpPage) {
        this.pageNum = this.jumpPage
        this.load()
      }
    },
  }
}
</script>

<style scoped>
.jump-page {
  margin-left: 20px;
  display: inline-flex;
  align-items: center;
  color: #606266;
  font-size: 13px;
}

.jump-page .el-input /deep/ .el-input__inner {
  text-align: center;
  padding: 0 5px;
}
</style>
