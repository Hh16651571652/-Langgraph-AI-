<template>
  <div class="reminder-container">
    <!-- 提醒按钮 -->
    <el-badge :value="overdueCount" :max="99" :hidden="overdueCount === 0" type="danger">
      <el-button 
        type="primary" 
        plain 
        circle 
        size="small" 
        @click="showReminderDialog = true"
        class="reminder-btn"
      >
        <el-icon><Bell /></el-icon>
      </el-button>
    </el-badge>

    <!-- 提醒弹窗 -->
    <el-dialog 
      v-model="showReminderDialog" 
      title="🕐 即将逾期任务提醒" 
      width="600px"
      :close-on-click-modal="false"
      append-to-body
    >
      <div class="reminder-content">
        <!-- 提醒统计 -->
        <div class="reminder-stats" v-if="totalTasks > 0">
          <el-alert 
            :title="`您有 ${totalTasks} 项任务即将逾期，请及时处理！`" 
            type="warning" 
            :closable="false"
            show-icon
          />
        </div>

        <!-- 任务列表 -->
        <div class="task-list" v-if="paginatedTasks.length > 0">
          <div 
            v-for="task in paginatedTasks" 
            :key="task.id" 
            class="task-item"
            :class="{ 'highlight': task.urgent }"
          >
            <div class="task-info">
              <div class="task-title">
                <strong>{{ task.title }}</strong>
                <el-tag 
                  v-if="task.urgent" 
                  size="small" 
                  type="danger" 
                  effect="dark"
                >
                  紧急
                </el-tag>
              </div>
              <div class="task-details">
                <span class="deadline">
                  <el-icon><Clock /></el-icon>
                  截止时间: {{ task.deadline }}
                </span>
                <span class="remaining-time">
                  <el-icon><Clock /></el-icon>
                  剩余时间: {{ task.remainingTime }}
                </span>
              </div>
              <div class="task-category">
                <el-tag size="small" :type="getCategoryType(task.category)">
                  {{ task.category }}
                </el-tag>
              </div>
            </div>
            <div class="task-actions">
              <el-button 
                type="primary" 
                size="small" 
                @click="handleViewTask(task)"
              >
                查看详情
              </el-button>
              <el-button 
                type="success" 
                size="small" 
                @click="handleMarkAsRead(task)"
              >
                标记已读
              </el-button>
            </div>
          </div>
        </div>

        <!-- 无提醒内容 -->
        <div v-else class="empty-state">
          <el-empty description="暂无即将逾期的任务">
            <template #image>
              <el-icon size="48" color="#67c23a"><SuccessFilled /></el-icon>
            </template>
          </el-empty>
        </div>

        <!-- 分页组件 -->
        <div class="pagination-container" v-if="totalTasks > 0">
          <!-- 左侧：总任务数 -->
          <div class="total-count">
            共 {{ totalTasks }} 条
          </div>
          
          <!-- 中间：每页显示选择器 -->
          <div class="page-size-selector">
            <span class="label">每页显示：</span>
            <el-select 
              v-model="pageSize" 
              size="small" 
              @change="handleSizeChange"
              class="page-size-select"
            >
              <el-option label="5条/页" :value="5" />
              <el-option label="10条/页" :value="10" />
              <el-option label="20条/页" :value="20" />
            </el-select>
          </div>
          
          <!-- 右侧：Element Plus 分页组件 -->
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[5, 10, 20]"
            :total="totalTasks"
            layout="prev, pager, next"
            small
            @current-change="handlePageChange"
          />
        </div>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showReminderDialog = false">关闭</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Bell, Clock, SuccessFilled } from '@element-plus/icons-vue'
import { getUpcomingOverdueTasks, markReminderAsRead } from '@/api/modules/reminder'

// 组件属性
defineProps({
  // 可以添加自定义属性，如提醒阈值等
})

// 响应式数据
const showReminderDialog = ref(false)
const overdueTasks = ref([])
const loading = ref(false)

// 分页相关数据
const currentPage = ref(1)
const pageSize = ref(5) // 每页显示5条任务
const totalTasks = ref(0)

// 计算属性
const overdueCount = computed(() => totalTasks.value)

// 当前显示的任务（直接使用后端返回的分页数据）
const paginatedTasks = computed(() => overdueTasks.value)

// 获取即将逾期任务（调用后端API）
const fetchUpcomingOverdueTasks = async () => {
  try {
    loading.value = true
    
    // 调用后端API，获取距离截止时间不到1小时的任务
    const response = await getUpcomingOverdueTasks({ 
      hours: 1.0,  // 1小时阈值
      page: currentPage.value,
      page_size: pageSize.value
    })
    
    console.log('[Reminder] API响应:', response)
    
    // API拦截器已经提取了response.data.data,所以response直接是后端的data对象
    // 后端返回格式: {total, page, page_size, todos}
    if (response && response.todos) {
      const rawData = response.todos || []
      totalTasks.value = response.total || 0
      
      // 字段映射：将后端数据转换为前端格式
      overdueTasks.value = rawData.map(task => ({
        ...task,
        deadline: formatDueDate(task.due_date),
        category: mapCategory(task.category),
        remainingTime: calculateRemainingTime(task.due_date),
        urgent: isUrgent(task.due_date)  // 距离截止<30分钟标记为紧急
      }))
      
      console.log('[Reminder] 即将逾期任务:', overdueTasks.value.length, '条')
    } else {
      console.warn('[Reminder] 响应格式异常:', response)
      overdueTasks.value = []
      totalTasks.value = 0
    }
    
  } catch (error) {
    console.error('[Reminder] 获取失败:', error)
    ElMessage.error('获取提醒任务失败: ' + error.message)
    // 错误时清空列表
    overdueTasks.value = []
    totalTasks.value = 0
  } finally {
    loading.value = false
  }
}

// 格式化截止时间
const formatDueDate = (dueDate) => {
  if (!dueDate) return '无'
  
  const date = new Date(dueDate)
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const day = date.getDate().toString().padStart(2, '0')
  const hours = date.getHours().toString().padStart(2, '0')
  const minutes = date.getMinutes().toString().padStart(2, '0')
  
  return `${month}-${day} ${hours}:${minutes}`
}

// 映射分类：英文 → 中文
const mapCategory = (category) => {
  const categoryMap = {
    'work': '工作',
    'study': '学习',
    'admin': '行政',
    'other': '其他',
    '工作': '工作',
    '学习': '学习',
    '行政': '行政',
    '其他': '其他'
  }
  return categoryMap[category] || '其他'
}

// 计算剩余时间
const calculateRemainingTime = (dueDate) => {
  if (!dueDate) return '未知'
  
  const now = new Date()
  const due = new Date(dueDate)
  const diffMs = due - now
  
  if (diffMs <= 0) return '已逾期'
  
  const diffMinutes = Math.floor(diffMs / (1000 * 60))
  const diffHours = Math.floor(diffMinutes / 60)
  
  if (diffHours > 0) {
    return `约${diffHours}小时`
  } else {
    return `约${diffMinutes}分钟`
  }
}

// 判断是否紧急（距离截止<30分钟）
const isUrgent = (dueDate) => {
  if (!dueDate) return false
  
  const now = new Date()
  const due = new Date(dueDate)
  const diffMs = due - now
  const diffMinutes = Math.floor(diffMs / (1000 * 60))
  
  return diffMinutes < 30 && diffMinutes > 0
}

// 获取分类标签类型
const getCategoryType = (category) => {
  const typeMap = {
    '工作': 'primary',
    '行政': 'success',
    '学习': 'warning',
    '其他': 'info'
  }
  return typeMap[category] || 'info'
}

// 查看任务详情
const handleViewTask = (task) => {
  ElMessage.info(`查看任务: ${task.title}`)
  // 这里可以跳转到任务详情页面或执行其他操作
  showReminderDialog.value = false
}

// 标记为已读
const handleMarkAsRead = async (task) => {
  try {
    await markReminderAsRead(task.id)
    overdueTasks.value = overdueTasks.value.filter(t => t.id !== task.id)
    ElMessage.success('已标记为已读')
  } catch (error) {
    ElMessage.error('标记失败: ' + error.message)
  }
}

// 分页大小改变事件
const handleSizeChange = (newSize) => {
  pageSize.value = newSize
  currentPage.value = 1 // 重置到第一页
  // 重新查询数据
  fetchUpcomingOverdueTasks()
}

// 页面切换事件
const handlePageChange = (newPage) => {
  currentPage.value = newPage
  // 重新查询数据
  fetchUpcomingOverdueTasks()
}

// 监听弹窗显示状态
watch(showReminderDialog, (newVal) => {
  if (newVal) {
    fetchUpcomingOverdueTasks()
  } else {
    // 弹窗关闭时重置分页状态
    currentPage.value = 1
    pageSize.value = 5
  }
})

// 组件挂载时获取提醒数据
onMounted(() => {
  fetchUpcomingOverdueTasks()
  
  // 定时刷新提醒数据（每5分钟）
  setInterval(() => {
    if (!showReminderDialog.value) {
      fetchUpcomingOverdueTasks()
    }
  }, 5 * 60 * 1000)
})

// 暴露方法给父组件
defineExpose({
  refreshReminders: fetchUpcomingOverdueTasks
})
</script>

<style scoped>
.reminder-container {
  display: inline-block;
}

.reminder-btn {
  font-size: 20px;
  padding: 8px;
}

.reminder-content {
  max-height: 400px;
  overflow-y: auto;
}

.reminder-stats {
  margin-bottom: 16px;
}

.task-list {
  space-y: 12px;
}

.task-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  margin-bottom: 8px;
  transition: all 0.3s;
}

.task-item.highlight {
  border-left: 4px solid #f56c6c;
  background-color: #fef0f0;
}

.task-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.task-info {
  flex: 1;
}

.task-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.task-details {
  display: flex;
  gap: 16px;
  margin-bottom: 8px;
  font-size: 12px;
  color: #909399;
}

.task-details i {
  margin-right: 4px;
}

.task-actions {
  display: flex;
  gap: 8px;
}

.empty-state {
  text-align: center;
  padding: 40px 0;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.pagination-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e4e7ed;
  gap: 16px;
}

.total-count {
  font-size: 14px;
  color: #606266;
  font-weight: 500;
  white-space: nowrap;
  flex-shrink: 0;
}

/* 每页显示选择器样式 */
.page-size-selector {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.page-size-selector .label {
  font-size: 14px;
  color: #606266;
  white-space: nowrap;
}

.page-size-select {
  width: 100px;
}

/* Element Plus 分页组件样式调整 */
:deep(.el-pagination) {
  margin: 0;
  flex-shrink: 0;
}

:deep(.el-pagination .btn-prev),
:deep(.el-pagination .btn-next) {
  padding: 0 8px;
}

:deep(.el-pagination .el-pager li) {
  min-width: 32px;
  height: 32px;
  line-height: 32px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .pagination-container {
    flex-direction: column;
    gap: 12px;
    align-items: center;
  }
  
  .page-size-selector {
    order: 2;
  }
  
  .total-count {
    order: 1;
  }
  
  :deep(.el-pagination) {
    order: 3;
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .task-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .task-actions {
    margin-top: 12px;
    width: 100%;
    justify-content: flex-end;
  }
  
  .task-details {
    flex-direction: column;
    gap: 4px;
  }
}
</style>