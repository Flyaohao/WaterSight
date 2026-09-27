<template>
  <div>
    <!-- 搜索区域 -->
    <div class="search">
      <!-- 输入框用于搜索活动名称 -->
      <el-input placeholder="请输入活动名称查询" style="width: 200px" v-model="name"></el-input>
      <!-- 点击按钮触发搜索 -->
<!--      plain 属性使得按钮在默认状态下背景色透明，只有边框和文字颜色，当鼠标悬停时，按钮背景色会变为信息色（info）-->
      <el-button type="info" plain style="margin-left: 10px" @click="load(1)">查询</el-button>
      <!-- 点击按钮重置搜索条件 -->
      <el-button type="warning" plain style="margin-left: 10px" @click="reset">重置</el-button>
    </div>

    <!-- 操作区域 -->
    <div class="operation">
      <!-- 点击按钮打开新增活动对话框 -->
      <el-button type="primary" plain @click="handleAdd">新增</el-button>
      <!-- 点击按钮批量删除选中活动 -->
      <el-button type="danger" plain @click="delBatch">批量删除</el-button>
    </div>

    <!-- 表格区域 -->
    <div class="table">
      <!-- 活动列表表格 -->
      <el-table :data="tableData" strip @selection-change="handleSelectionChange">
        <!-- 选择框列 -->
        <el-table-column type="selection" width="55" align="center"></el-table-column>
        <!-- 序号列 -->
        <el-table-column prop="id" label="序号" width="70" align="center" sortable></el-table-column>
        <!-- 活动名称列 -->
        <el-table-column prop="name" label="活动名称"></el-table-column>
        <!-- 活动简介列，内容过长时显示省略号 -->
        <el-table-column prop="descr" label="活动简介" show-overflow-tooltip></el-table-column>
        <!-- 封面列，显示图片 -->
        <el-table-column prop="cover" label="封面">
          <template v-slot="scope">
            <div style="display: flex; align-items: center">
              <el-image style="width: 50px; height: 30px; border-radius: 5px" v-if="scope.row.cover"
                        :src="scope.row.cover" :preview-src-list="[scope.row.cover]"></el-image>
            </div>
          </template>
        </el-table-column>
        <!-- 开始时间列 -->
        <el-table-column prop="start" label="开始时间"></el-table-column>
        <!-- 结束时间列 -->
        <el-table-column prop="end" label="结束时间"></el-table-column>
        <!-- 活动形式列 -->
        <el-table-column prop="form" label="活动形式"></el-table-column>
        <!-- 活动地址列，内容过长时显示省略号 -->
        <el-table-column prop="address" label="活动地址" show-overflow-tooltip></el-table-column>
        <!-- 主办方列 -->
        <el-table-column prop="host" label="主办方"></el-table-column>
        <!-- 浏览量列 -->
        <el-table-column prop="readCount" label="浏览量"></el-table-column>

        <!-- 查看活动详情按钮列 -->
        <el-table-column label="查看活动详情" width="140">
          <template v-slot="scope">
            <el-button @click="preview(scope.row.content)">查看活动详情</el-button>
          </template>
        </el-table-column>

        <!-- 操作按钮列 -->
        <el-table-column label="操作" align="center" width="180">
          <template v-slot="scope">
            <el-button size="mini" type="primary" plain @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="mini" type="danger" plain @click="del(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页区域 -->
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


    <!-- 新增或编辑活动对话框 -->
    <el-dialog title="信息" :visible.sync="fromVisible" width="60%" :close-on-click-modal="false" destroy-on-close>
      <!-- 表单用于输入活动信息 -->
      <el-form :model="form" label-width="100px" style="padding-right: 50px" :rules="rules" ref="formRef">
        <!-- 活动名称输入框 -->
        <el-form-item label="活动名称" prop="name">
          <el-input v-model="form.name" placeholder="活动名称"></el-input>
        </el-form-item>
        <!-- 活动简介输入框 -->
        <el-form-item label="活动简介" prop="descr">
          <el-input type="textarea" v-model="form.descr" placeholder="活动简介"></el-input>
        </el-form-item>
        <!-- 封面上传 -->
        <el-form-item label="封面" prop="cover">
          <el-upload
              :action="$baseUrl + '/files/upload'"
              :headers="{ token: user.token }"
              list-type="picture"
              :on-success="handleCoverSuccess"
          >
            <el-button type="primary">上传封面</el-button>
          </el-upload>
        </el-form-item>
        <!-- 开始时间选择框 -->
        <el-form-item label="开始时间" prop="start">
          <el-date-picker style="width: 100%" value-format="yyyy-MM-dd" format="yyyy-MM-dd" v-model="form.start" placeholder="开始时间"></el-date-picker>
        </el-form-item>
        <!-- 结束时间选择框 -->
        <el-form-item label="结束时间" prop="end">
          <el-date-picker style="width: 100%" value-format="yyyy-MM-dd" format="yyyy-MM-dd" v-model="form.end" placeholder="结束时间"></el-date-picker>
        </el-form-item>
        <!-- 活动形式选择框 -->
        <el-form-item label="活动形式" prop="form">
          <el-select style="width: 100%" v-model="form.form">
            <el-option value="线上"></el-option>
            <el-option value="线下"></el-option>
          </el-select>
        </el-form-item>
        <!-- 活动地址输入框 -->
        <el-form-item label="活动地址" prop="address">
          <el-input v-model="form.address" placeholder="活动地址"></el-input>
        </el-form-item>
        <!-- 主办方输入框 -->
        <el-form-item label="主办方" prop="host">
          <el-input v-model="form.host" placeholder="主办方"></el-input>
        </el-form-item>
        <!-- 活动内容编辑器 -->
        <el-form-item label="内容" prop="content">
          <div id="editor"></div>
        </el-form-item>
      </el-form>
      <!-- 对话框底部按钮 -->
      <div slot="footer" class="dialog-footer">
        <el-button @click="fromVisible = false">取 消</el-button>
        <el-button type="primary" @click="save">确 定</el-button>
      </div>
    </el-dialog>

    <!-- 活动详情对话框 -->
    <el-dialog title="活动详情" :visible.sync="fromVisible1" width="50%" :close-on-click-modal="false" :append-to-body="true" destroy-on-close>
      <!-- 显示活动详情内容 -->
      <div class="w-e-text">
        <div v-html="content"></div>
      </div>

      <!-- 对话框底部按钮 -->
      <div slot="footer" class="dialog-footer">
        <el-button @click="fromVisible1 = false">关 闭</el-button>
      </div>
    </el-dialog>

  </div>
</template>


<script>
import E from "wangeditor"
import hljs from 'highlight.js'

export default {
  name: "Activity",
  data() {
    return {
      tableData: [],  // 所有的数据
      pageNum: 1,   // 当前的页码
      pageSize: 10,  // 每页显示的个数
      total: 0,
      name: null,
      fromVisible: false,
      form: {},
      user: JSON.parse(localStorage.getItem('xm-user') || '{}'),
      rules: {
        name: [
          {required: true, message: '请输入活动名称', trigger: 'blur'},
        ],
        descr: [
          {required: true, message: '请输入活动简介', trigger: 'blur'},
        ],
        start: [
          {required: true, message: '请输入活动开始时间', trigger: 'blur'},
        ],
        end: [
          {required: true, message: '请输入活动结束时间', trigger: 'blur'},
        ],
        address: [
          {required: true, message: '请输入活动地址', trigger: 'blur'},
        ],
        host: [
          {required: true, message: '请输入活动主办方', trigger: 'blur'},
        ],
      },
      ids: [],
      editor: null,
      content: '',
      fromVisible1: false,
      jumpPage: 1,
    }
  },
  created() {
    this.load(1)
  },
  methods: {
    preview(content) {
      this.content = content
      this.fromVisible1 = true
    },
    handleAdd() {   // 新增数据
      this.form = {}  // 新增数据的时候清空数据
      this.fromVisible = true   // 打开弹窗
      this.setRichText('')
    },
    handleEdit(row) {   // 编辑数据
      this.form = JSON.parse(JSON.stringify(row))  // 给form对象赋值  注意要深拷贝数据
      this.fromVisible = true   // 打开弹窗
      this.setRichText(this.form.content)
    },
    save() {   // 保存按钮触发的逻辑  它会触发新增或者更新
      this.$refs.formRef.validate((valid) => {
        if (valid) {
          this.form.content = this.editor.txt.html()
          this.$request({
            url: this.form.id ? '/activity/update' : '/activity/add',
            method: this.form.id ? 'PUT' : 'POST',
            data: this.form
          }).then(res => {
            if (res.code === '200') {  // 表示成功保存
              this.$message.success('保存成功')
              this.load(1)
              this.fromVisible = false
            } else {
              this.$message.error(res.msg)  // 弹出错误的信息
            }
          })
        }
      })
    },
    del(id) {   // 单个删除
      this.$confirm('您确定删除吗？', '确认删除', {type: "warning"}).then(response => {
        this.$request.delete('/activity/delete/' + id).then(res => {
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
        this.$request.delete('/activity/delete/batch', {data: this.ids}).then(res => {
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
    /**
     * 分页加载活动数据
     *
     * 该方法用于根据当前页码、页面大小和活动名称查询活动列表
     * 如果提供了新的页码，则更新当前页码，并发起网络请求获取数据
     *
     * @param {number} pageNum - 可选参数，如果提供，则更新当前页码为该值
     */
    load(pageNum) {
      // 更新当前页码，如果提供了pageNum参数
      if (pageNum) this.pageNum = pageNum

      // 发起GET请求，使用当前页码、页面大小和活动名称作为查询参数
      this.$request.get('/activity/selectPage', {
        params: {
          pageNum: this.pageNum,
          pageSize: this.pageSize,
          name: this.name,
        }
      }).then(res => {
        // 更新表格数据和总记录数
        this.tableData = res.data?.list
        this.total = res.data?.total
      })
    },
    /**
     * 重置组件状态
     * 此方法将名称属性重置为null，并重新加载数据
     */
    reset() {
      // 将名称属性重置为null
      this.name = null
      // 重新加载数据，参数1表示加载第一页数据
      this.load(1)
    },
    /**
     * 当前页码变更时的处理函数
     * @param {number} pageNum - 用户选择的新的页码
     */
    handleCurrentChange(pageNum) {
      // 加载指定页码的数据
      this.load(pageNum)
    },
    /**
     * 处理封面上传成功后的回调函数
     * @param {Object} res - 上传接口返回的结果对象，包含上传的文件数据
     */
    handleCoverSuccess(res) {
      this.form.cover = res.data
    },

    /**
     * 设置富文本编辑器的内容
     * 在富文本编辑器实例化后，设置编辑器的内容
     * @param {String} content - 要设置的富文本内容
     */
    setRichText(content) {
      this.$nextTick(() => {
        // 初始化富文本编辑器
        this.editor = new E(`#editor`)
        // 设置编辑器的代码高亮功能
        this.editor.highlight = hljs
        // 配置编辑器的图片上传服务器地址
        this.editor.config.uploadImgServer = this.$baseUrl + '/files/editor/upload'
        // 配置图片上传时的文件参数名称
        this.editor.config.uploadFileName = 'file'
        // 配置图片上传时的请求头，包含用户token用于身份验证
        this.editor.config.uploadImgHeaders = {
          token: this.user.token
        }
        // 配置图片上传时的额外参数
        this.editor.config.uploadImgParams = {
          type: 'img',
        }
        // 创建富文本编辑器实例
        this.editor.create()
        // 设置富文本编辑器的内容
        this.editor.txt.html(content)
      })
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
