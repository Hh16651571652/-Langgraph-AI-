<template>
  <div>
    <div class="card">
      <div class="card-header">
        <h3>📋 待办事项 · 智能看板</h3>
        <div class="header-actions">
          <!-- 历史记录按钮 -->
          <el-button 
            type="info" 
            plain 
            size="small" 
            @click="showHistoryDialog = true" 
            class="history-btn"
          >
            <el-icon><Clock /></el-icon>
            历史记录
          </el-button>
          <!-- 提醒按钮组件 -->
          <ReminderButton ref="reminderButtonRef" />
          <el-button type="text" size="small" @click="refreshTodos" class="refresh-btn">
            <el-icon><Refresh /></el-icon>
          </el-button>
        </div>
      </div>
      <!-- 统计图表与优化建议 -->
      <!-- 待办任务区域 -->
      <div v-if="!showCompletedTasks" class="grid-2col">
        <div>
          <div id="todoChart"></div>
          <div class="progress-bar-container">
            <div class="progress-bar">
              <div class="progress-fill" :style="{width: todoStats.completionRate+'%'}"></div>
            </div>
            <p style="font-size:13px; color:#4a6a8a; margin-top: 4px;">
              ✅ 完成率 {{todoStats.completionRate}}%  |  建议: {{todoStats.suggestion}}
            </p>
          </div>
        </div>
        <div>
          <div v-for="task in paginatedTasks" :key="task.id" class="task-item">
            <div>
              <strong>{{ task.title }}</strong><br>
              <small>
                截止: {{ task.deadline }} | {{ task.category }}
              </small>
            </div>
            <div style="display: flex; gap: 6px;">
              <span 
                class="task-status" 
                :class="getStatusClass(task.status)"
              >
                {{ task.status }}
              </span>
              <!-- 勾选按钮，仅对未完成且非逾期的任务显示 -->
              <button 
                v-if="task.status !== '逾期'" 
                class="check-btn" 
                @click="markTaskAsCompleted(task)"
                :title="'标记为已完成'"
              >
                <el-icon><Check /></el-icon>
              </button>
            </div>
          </div>
          
          <!-- 分页组件 -->
          <div class="pagination-container" v-if="pendingTasks.length > 0">
            <!-- 左侧：总任务数 -->
            <div class="total-count">
              共 {{ pendingTasks.length }} 条待办任务
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
              :total="pendingTasks.length"
              layout="prev, pager, next"
              size="small"
              @current-change="handlePageChange"
            />
          </div>
        </div>
      </div>


      <!-- 历史记录弹窗 -->
       <el-dialog 
         v-model="showHistoryDialog" 
         title="📚 历史记录" 
         width="800px"
         :close-on-click-modal="true"
       >
         <div class="history-dialog">
           <!-- 筛选工具栏 -->
           <div class="filter-toolbar">
             <div class="filter-left">
               <span class="filter-label">状态筛选：</span>
               <el-radio-group v-model="historyFilter" size="small">
                 <el-radio-button label="all">全部</el-radio-button>
                 <el-radio-button label="completed">已完成</el-radio-button>
                 <el-radio-button label="overdue">逾期</el-radio-button>
               </el-radio-group>
             </div>
             <div class="filter-right">
               <span class="total-count">共 {{ filteredHistoryTasks.length }} 条记录</span>
             </div>
           </div>

           <!-- 历史记录列表 -->
            <div class="history-tasks-list" v-if="filteredHistoryTasks.length > 0">
             <div 
               v-for="task in paginatedHistoryTasks" 
               :key="task.id" 
               class="history-task-item"
               :class="{ 'completed-task': task.status === '已完成', 'overdue-task': task.status === '逾期' }"
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
                   <span class="completion-time" v-if="task.status === '已完成'">
                     <el-icon><Clock /></el-icon>
                     完成时间: {{ formatCompletionTime(task.completionTime) }}
                   </span>
                   <span class="original-deadline">
                     <el-icon><Calendar /></el-icon>
                     原定截止: {{ task.deadline }}
                   </span>
                 </div>
                 <div class="task-category">
                   <el-tag size="small" :type="getCategoryType(task.category)">
                     {{ task.category }}
                   </el-tag>
                 </div>
               </div>
               <div class="task-actions">
                 <!-- 逾期任务显示标记为完成按钮 -->
                 <button 
                   v-if="task.status === '逾期'" 
                   class="complete-overdue-btn" 
                   @click="markOverdueAsCompleted(task)"
                   title="标记为已完成"
                 >
                   <el-icon><Check /></el-icon>
                   完成
                 </button>
                 <span :class="getStatusClass(task.status)">{{ task.status }}</span>
               </div>
             </div>
           </div>

           <!-- 分页组件 -->
           <div class="pagination-container" v-if="filteredHistoryTasks.length > 0">
             <div class="total-count">
               共 {{ filteredHistoryTasks.length }} 条记录
             </div>
             
             <div class="page-size-selector">
               <span class="label">每页显示：</span>
               <el-select 
                 v-model="historyPageSize" 
                 size="small" 
                 @change="handleHistorySizeChange"
                 class="page-size-select"
               >
                 <el-option label="5条/页" :value="5" />
                 <el-option label="10条/页" :value="10" />
                 <el-option label="20条/页" :value="20" />
               </el-select>
             </div>
             
             <el-pagination
               v-model:current-page="historyCurrentPage"
               v-model:page-size="historyPageSize"
               :page-sizes="[5, 10, 20]"
               :total="filteredHistoryTasks.length"
               layout="prev, pager, next"
               size="small"
               @current-change="handleHistoryPageChange"
             />
           </div>

           <!-- 无历史记录 -->
           <div v-else class="empty-state">
             <el-empty description="暂无历史记录">
               <template #image>
                 <el-icon size="48" color="#909399"><List /></el-icon>
               </template>
             </el-empty>
           </div>
         </div>
         
         <template #footer>
           <span class="dialog-footer">
             <el-button @click="showHistoryDialog = false">关闭</el-button>
           </span>
         </template>
      </el-dialog>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh, Check, Clock, Calendar, List } from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import { getTodoList, updateTodoStatus, getTodoStats } from '@/api/modules/todo'
import ReminderButton from '@/components/ReminderButton.vue'

// 获取路由对象
const route = useRoute()
const router = useRouter()

// 提醒按钮引用
const reminderButtonRef = ref()

// 历史记录弹窗显示状态
const showHistoryDialog = ref(false)

// 历史记录筛选状态
const historyFilter = ref('all') // all: 全部, completed: 已完成, overdue: 逾期

// 是否显示已完成任务（用于切换视图）
const showCompletedTasks = ref(false)

// 分页相关数据 - 待办任务
const currentPage = ref(1)
const pageSize = ref(5) // 每页显示5条任务
const totalTasks = ref(0)

// 分页相关数据 - 历史记录
const historyCurrentPage = ref(1)
const historyPageSize = ref(5) // 每页显示5条历史记录

// 已完成任务列表
const completedTasks = computed(() => {
  return todoList.value.filter(task => task.status === '已完成')
})

// 逾期任务列表
const overdueTasks = computed(() => {
  return todoList.value.filter(task => task.status === '逾期')
})

// 历史记录任务列表（已完成 + 逾期）
const historyTasks = computed(() => {
  return todoList.value.filter(task => task.status === '已完成' || task.status === '逾期')
})

// 筛选后的历史记录任务列表
const filteredHistoryTasks = computed(() => {
  if (historyFilter.value === 'completed') {
    return completedTasks.value
  } else if (historyFilter.value === 'overdue') {
    return overdueTasks.value
  } else {
    return historyTasks.value
  }
})

// 待办任务列表（未完成的任务）
const pendingTasks = computed(() => {
  return todoList.value.filter(task => task.status !== '已完成' && task.status !== '逾期')
})

// 计算当前页显示的待办任务
const paginatedTasks = computed(() => {
  const startIndex = (currentPage.value - 1) * pageSize.value
  const endIndex = startIndex + pageSize.value
  return pendingTasks.value.slice(startIndex, endIndex)
})

// 计算当前页显示的历史记录任务
const paginatedHistoryTasks = computed(() => {
  const startIndex = (historyCurrentPage.value - 1) * historyPageSize.value
  const endIndex = startIndex + historyPageSize.value
  return filteredHistoryTasks.value.slice(startIndex, endIndex)
})

// 代办数据
const todoList = ref([])
const todoStats = ref({
  completionRate: 0,
  suggestion: '优先处理逾期任务'
})

// 获取代办列表
const fetchTodoList = async () => {
  try {
    const response = await getTodoList()
    
    // API拦截器已经提取了response.data.data,所以response直接是数组
    const rawData = Array.isArray(response) ? response : []
    
    // 字段映射: 将后端字段转换为前端期望的格式
    todoList.value = rawData.map(task => {
      // 根据当前时间和截止时间动态判断状态
      let displayStatus = task.status
      
      if (task.status === 'pending') {
        if (task.due_date) {
          const now = new Date()
          const dueDate = new Date(task.due_date)
          if (now > dueDate) {
            displayStatus = '逾期'  // 超过截止时间,显示为逾期
          } else {
            displayStatus = '进行中'
          }
        } else {
          // 如果没有截止时间，默认为进行中
          displayStatus = '进行中'
        }
      } else if (task.status === 'completed') {
        displayStatus = '已完成'
      } else if (task.status === 'cancelled') {
        displayStatus = '已取消'
      }
      
      return {
        ...task,
        status: displayStatus,  // 使用动态计算的状态
        deadline: formatDueDate(task.due_date),        // due_date → deadline
        category: mapCategory(task.category),          // 英文分类 → 中文分类
        completionTime: task.completed_at              // completed_at → completionTime (用于历史记录)
      }
    })
  } catch (error) {
    console.error('[Todo] 获取失败:', error)
    ElMessage.error('获取代办列表失败: ' + error.message)
    // 错误时设置为空数组,不使用模拟数据
    todoList.value = []
  }
}

// 格式化截止时间
const formatDueDate = (dueDate) => {
  if (!dueDate) {
    return '无'
  }
  
  try {
    const date = new Date(dueDate)
    
    // 检查日期是否有效
    if (isNaN(date.getTime())) {
      return '无'
    }
    
    const month = (date.getMonth() + 1).toString().padStart(2, '0')
    const day = date.getDate().toString().padStart(2, '0')
    const hours = date.getHours().toString().padStart(2, '0')
    const minutes = date.getMinutes().toString().padStart(2, '0')
    
    return `${month}-${day} ${hours}:${minutes}`
  } catch (error) {
    console.error('[Todo] 日期格式化失败:', error, dueDate)
    return '无'
  }
}

// 映射分类: 英文 → 中文
const mapCategory = (category) => {
  const categoryMap = {
    'work': '工作',
    'study': '学习',
    'admin': '行政',
    'other': '其他',
    '工作': '工作',  // 兼容已经是中文的情况
    '学习': '学习',
    '行政': '行政',
    '其他': '其他'
  }
  return categoryMap[category] || '其他'
}

// 获取统计信息
const fetchTodoStats = async () => {
  try {
    const response = await getTodoStats()
    // API拦截器已经提取了response.data.data,所以response直接是对象
    const statsData = response || {}
    
    // 只统计"进行中"和"已完成"的任务(排除逾期)
    const ongoingTasks = todoList.value.filter(task => task.status === '进行中')
    const completedTasks = todoList.value.filter(task => task.status === '已完成')
    const overdueTasks = todoList.value.filter(task => task.status === '逾期')
    
    // 计算完成率: (总任务数 - 逾期 - 未完成) / 总任务数
    // 即: 1 - (逾期 + 未完成) / 总数
    const totalTasks = todoList.value.length
    const incompleteTasks = ongoingTasks.length + overdueTasks.length
    const completionRate = totalTasks > 0 ? Math.round(((totalTasks - incompleteTasks) / totalTasks) * 100) : 0
    
    // 生成建议文案 - 针对所有未完成任务
    let suggestion = ''
    if (totalTasks === 0) {
      suggestion = '暂无任务，添加一个新任务吧 ✨'
    } else if (overdueTasks.length > 0) {
      suggestion = `有${overdueTasks.length}个任务已逾期，请优先处理 ⚠️`
    } else if (ongoingTasks.length > 0) {
      suggestion = `还有${ongoingTasks.length}个任务未完成，快加油吧 💪`
    } else {
      suggestion = '太棒了！所有任务都已完成 🎉'
    }
    
    todoStats.value = {
      completionRate,
      suggestion,
      ...statsData
    }
  } catch (error) {
    console.error('[Todo] 统计获取失败:', error)
    ElMessage.error('获取统计信息失败: ' + error.message)
    // 错误时使用默认值
    todoStats.value = {
      completionRate: 0,
      suggestion: '暂无数据',
      pending_count: 0,
      completed_count: 0,
      cancelled_count: 0,
      total_count: 0
    }
  }
}

// 分页大小改变事件 - 待办任务
const handleSizeChange = (newSize) => {
  pageSize.value = newSize
  currentPage.value = 1 // 重置到第一页
}

// 页面切换事件 - 待办任务
const handlePageChange = (newPage) => {
  currentPage.value = newPage
}

// 分页大小改变事件 - 历史记录
const handleHistorySizeChange = (newSize) => {
  historyPageSize.value = newSize
  historyCurrentPage.value = 1 // 重置到第一页
}

// 页面切换事件 - 历史记录
const handleHistoryPageChange = (newPage) => {
  historyCurrentPage.value = newPage
}

// 获取状态对应的CSS类名
const getStatusClass = (status) => {
  if (status === '已完成') return 'status-done'
  if (status === '逾期') return 'status-overdue'
  return 'status-progress'
}

// 格式化完成时间
const formatCompletionTime = (completionTime) => {
  if (!completionTime) return '未知时间'
  
  const date = new Date(completionTime)
  // 格式化为 YY-MM-DD HH:MM:SS
  const year = date.getFullYear().toString().slice(-2)
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const day = date.getDate().toString().padStart(2, '0')
  const hours = date.getHours().toString().padStart(2, '0')
  const minutes = date.getMinutes().toString().padStart(2, '0')
  const seconds = date.getSeconds().toString().padStart(2, '0')
  
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}

// 获取任务类别对应的颜色
const getCategoryColor = (category) => {
  const colorMap = {
    '工作': '#2b6ef0',    // 蓝色
    '行政': '#10b981',    // 绿色
    '学习': '#f59e0b',    // 橙色
    '其他': '#8b5cf6'     // 紫色
  }
  return colorMap[category] || '#6b7280'
}

// 获取任务类别对应的Element Plus标签类型
const getCategoryType = (category) => {
  const typeMap = {
    '工作': 'primary',
    '行政': 'success', 
    '学习': 'warning',
    '其他': 'info'
  }
  return typeMap[category] || 'info'
}

// 标记任务为已完成
const markTaskAsCompleted = async (task) => {
  try {
    // 确认对话框
    await ElMessageBox.confirm(
      `确定要将任务“${task.title}”标记为已完成吗？`,
      '确认完成',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    // 记录完成时间
    const completionTime = new Date().toISOString()
    
    // 传递英文状态给后端
    await updateTodoStatus(task.id, 'completed', completionTime)
    ElMessage.success(`任务“${task.title}”已标记为完成`)
    
    // 重新获取数据
    await refreshTodos()
    
    // 刷新提醒数据
    if (reminderButtonRef.value) {
      reminderButtonRef.value.refreshReminders()
    }
  } catch (error) {
    // 用户点击取消时，不显示错误信息
    if (error !== 'cancel') {
      ElMessage.error('标记任务完成失败: ' + error.message)
    }
  }
}

// 更新任务状态（保留原有功能，用于其他状态切换）
const updateTaskStatus = async (id, currentStatus) => {
  try {
    let newStatus
    // 前端显示状态 -> 后端英文状态的映射
    if (currentStatus === '已完成') newStatus = 'pending'  // 从完成改回待处理
    else if (currentStatus === '进行中') newStatus = 'completed'  // 从待处理改为完成
    else if (currentStatus === '逾期') newStatus = 'pending'  // 从逾期改回待处理
    else newStatus = 'pending'
    
    await updateTodoStatus(id, newStatus)
    ElMessage.success('状态已更新，并同步至协作方')
    
    // 重新获取数据
    await refreshTodos()
    
    // 刷新提醒数据
    if (reminderButtonRef.value) {
      reminderButtonRef.value.refreshReminders()
    }
  } catch (error) {
    ElMessage.error('更新状态失败: ' + error.message)
  }
}

// 将逾期任务标记为已完成
const markOverdueAsCompleted = async (task) => {
  try {
    // 显示确认弹窗
    await ElMessageBox.confirm(
      `确定要将逾期任务“${task.title}”标记为已完成吗？`,
      '✅ 确认完成',
      {
        confirmButtonText: '确认完成',
        cancelButtonText: '取消',
        type: 'success',
        distinguishCancelAndClose: true
      }
    )
    
    // 记录完成时间
    const completionTime = new Date().toISOString()
    
    // 调用API更新状态（传递英文状态）
    await updateTodoStatus(task.id, 'completed', completionTime)
    ElMessage.success(`任务“${task.title}”已标记为完成`)
    
    // 重新获取数据
    await refreshTodos()
    
    // 刷新提醒数据
    if (reminderButtonRef.value) {
      reminderButtonRef.value.refreshReminders()
    }
  } catch (error) {
    // 用户点击取消时，不显示错误信息
    if (error !== 'cancel' && error !== 'close') {
      ElMessage.error('标记任务完成失败: ' + error.message)
    }
  }
}

// 刷新待办统计图表
const refreshTodos = async () => {
  await Promise.all([fetchTodoList(), fetchTodoStats()])
  nextTick(() => renderTodoChart())
}

// 渲染图表
const renderTodoChart = () => {
  const chartDom = document.getElementById('todoChart')
  if (!chartDom) return
  
  const chart = echarts.init(chartDom)
  
  // 只统计“进行中”的任务(排除已完成和逾期)
  const ongoingTasks = todoList.value.filter(task => task.status === '进行中')
  
  // 按类别统计进行中的任务数量
  const categories = ['工作', '行政', '学习', '其他']
  const data = categories.map(cat => 
    ongoingTasks.filter(task => task.category === cat).length
  )
  
  chart.setOption({
    tooltip: {},
    graphic: {
      elements: categories.map((category, index) => ({
        type: 'group',
        right: 10,
        top: 10 + index * 20,
        children: [
          {
            type: 'rect',
            left: 0,
            top: 0,
            shape: { width: 12, height: 12 },
            style: { fill: getCategoryColor(category) }
          },
          {
            type: 'text',
            left: 18,
            top: 6,
            style: { 
              text: category, 
              fontSize: 10, 
              fill: '#606266' 
            }
          }
        ]
      }))
    },
    grid: {
      top: '5%',
      left: '10%',
      right: '10%',
      bottom: '20%',
      containLabel: true
    },
    xAxis: { 
      data: categories,
      axisLabel: {
        interval: 0
      }
    },
    yAxis: { 
      type: 'value',
      interval: 1,
      axisLabel: {
        margin: 8
      }
    },
    series: [{
      type: 'bar',
      data: data.map((value, index) => ({
        value: value,
        itemStyle: {
          color: getCategoryColor(categories[index])
        }
      })),
      itemStyle: { 
        borderRadius: [8, 8, 0, 0]
      },
      barWidth: '60%'
    }]
  })
}

// 检查并显示待办提醒
const checkAndShowTodoReminders = () => {
  const now = new Date()
  
  // 统计逾期任务
  const overdueTasks = todoList.value.filter(task => task.status === '逾期')
  
  // 统计即将截止的任务（24小时内）
  const upcomingTasks = todoList.value.filter(task => {
    if (task.status !== '进行中' || !task.due_date) return false
    
    const dueDate = new Date(task.due_date)
    const hoursDiff = (dueDate - now) / (1000 * 60 * 60) // 转换为小时
    
    // 24小时内且未过期
    return hoursDiff > 0 && hoursDiff <= 24
  })
  
  // 构建提醒消息
  const messages = []
  
  if (overdueTasks.length > 0) {
    messages.push(`⚠️ 有 ${overdueTasks.length} 条待办事项已逾期，请到历史记录中查看`)
  }
  
  if (upcomingTasks.length > 0) {
    messages.push(`⏰ 有 ${upcomingTasks.length} 条待办事项即将截止，请加急完成`)
  }
  
  // 如果有需要提醒的事项，显示弹窗
  if (messages.length > 0) {
    ElMessageBox.alert(
      messages.join('<br><br>'),
      '📋 待办提醒',
      {
        confirmButtonText: '知道了',
        type: messages.length > 1 ? 'warning' : 'info',
        dangerouslyUseHTMLString: true,
        customClass: 'todo-reminder-dialog'
      }
    )
  }
}

onMounted(async () => {
  await refreshTodos()
  
  // 如果从 NLP命令跳转过来（带有refresh参数），显示提示信息
  if (route.query.refresh === 'true' || route.query.refresh === true) {
    ElMessage.success('✅ 新任务已添加到待办列表！')
  } else {
    // 首次加载时，检查并显示待办提醒
    checkAndShowTodoReminders()
  }
})

// 监听路由变化，当从 Layout 的 NLP 输入框跳转过来时刷新数据
watch(
  () => route.query.refresh,
  async (newVal, oldVal) => {
    // 只要 newVal 为 true 就刷新，不管 oldVal 是什么
    if (newVal === 'true' || newVal === true) {
      console.log('[Todo] 检测到refresh参数，刷新数据...')
      await refreshTodos()
      ElMessage.success('✅ 待办列表已更新！')
      
      // 刷新完成后，清除 query 参数，防止下次进入误判
      router.replace({ query: {} })
    }
  },
  { flush: 'post' } // 确保在 DOM 更新后执行
)
</script>

<style scoped>
.card {
  background: var(--bg-card);
  border-radius: 24px;
  padding: 20px 24px;
  margin-bottom: 24px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-light);
  transition: 0.1s;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
  border-left: 4px solid var(--primary);
  padding-left: 14px;
}

.card-header h3 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.refresh-btn {
  font-size: 16px;
  padding: 8px;
  width: 40px;
  height: 40px;
}

.grid-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  align-items: start;
}

/* 左侧统计图表容器 */
.grid-2col > div:first-child {
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%;
}

/* 统计图表样式 */
#todoChart {
  height: 200px !important;
  margin-bottom: 8px;
}

/* 完成率进度条容器 */
.progress-bar-container {
  margin-top: 8px;
}

.task-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #eef2ff;
}

.task-status {
  padding: 4px 12px;
  border-radius: 40px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-done { 
  background: #d4edda; 
  color: #155724; 
}

.status-progress { 
  background: #fff3cd; 
  color: #856404; 
}

.status-overdue { 
  background: #f8d7da; 
  color: #721c24; 
}

.btn-sm {
  background: #eef3ff;
  border: none;
  border-radius: 30px;
  padding: 4px 12px;
  cursor: pointer;
  color: var(--primary);
}

.check-btn {
  background: #10b981;
  border: none;
  border-radius: 50%;
  padding: 6px;
  cursor: pointer;
  color: white;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.check-btn:hover {
  background: #059669;
  transform: scale(1.05);
}

/* 历史记录弹窗样式 */
.history-dialog {
  max-height: 500px;
  overflow-y: auto;
}

.filter-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding: 12px 0;
  border-bottom: 1px solid #eef2ff;
}

.filter-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.filter-label {
  font-size: 0.9rem;
  color: #606266;
  font-weight: 500;
}

.filter-right {
  font-size: 0.9rem;
  color: #909399;
}

.history-tasks-list {
  max-height: 400px;
  overflow-y: auto;
}

.history-task-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  margin-bottom: 12px;
  background: #f8f9fa;
  border-radius: 12px;
  transition: all 0.2s;
}

.completed-task {
  border-left: 4px solid #10b981;
}

.overdue-task {
  border-left: 4px solid #f56565;
}

.history-task-item:hover {
  background: #f1f5f9;
  transform: translateY(-1px);
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

.task-title strong {
  font-size: 1rem;
  color: #374151;
}

.completed-task .task-title strong {
  text-decoration: line-through;
  color: #6b7280;
}

.task-details {
  display: flex;
  gap: 16px;
  font-size: 0.85rem;
  color: #6b7280;
  margin-bottom: 8px;
}

.completion-time,
.original-deadline {
  display: flex;
  align-items: center;
  gap: 4px;
}

.task-category {
  margin-top: 4px;
}

.task-status {
  margin-left: 12px;
}

/* 任务操作区域 */
.task-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-left: 12px;
}

/* 逾期任务完成按钮 */
.complete-overdue-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 4px rgba(16, 185, 129, 0.2);
}

.complete-overdue-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(16, 185, 129, 0.3);
}

.complete-overdue-btn:active {
  transform: translateY(0);
}

.status-done {
  background: #d4edda;
  color: #155724;
  padding: 4px 12px;
  border-radius: 40px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-overdue {
  background: #f8d7da;
  color: #721c24;
  padding: 4px 12px;
  border-radius: 40px;
  font-size: 0.75rem;
  font-weight: 500;
}

.empty-state {
  text-align: center;
  padding: 40px 0;
}

.completed-task {
  opacity: 0.7;
  background: #f8f9fa;
  border-left: 4px solid #10b981;
}

.completed-task strong {
  text-decoration: line-through;
  color: #6b7280;
}

.progress-bar {
  width: 100%;
  height: 6px;
  background: #e2e8f0;
  border-radius: 10px;
  margin-top: 10px;
}

.progress-fill {
  width: 0%;
  height: 100%;
  background: var(--primary);
  border-radius: 10px;
  transition: width 0.3s;
}

.mt-2 {
  margin-top: 0.5rem;
}

/* 分页组件样式 */
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

@media (max-width: 768px) {
  .grid-2col {
    grid-template-columns: 1fr;
  }
  
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .header-actions {
    width: 100%;
    justify-content: flex-end;
  }
  
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

/* 待办提醒弹窗样式 */
:deep(.todo-reminder-dialog) {
  border-radius: 16px;
}

:deep(.todo-reminder-dialog .el-message-box__header) {
  padding: 20px 20px 10px;
}

:deep(.todo-reminder-dialog .el-message-box__title) {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

:deep(.todo-reminder-dialog .el-message-box__content) {
  padding: 10px 20px 20px;
  font-size: 15px;
  line-height: 1.8;
  color: #606266;
}

:deep(.todo-reminder-dialog .el-message-box__btns) {
  padding: 10px 20px 20px;
}

:deep(.todo-reminder-dialog .el-button--primary) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 8px;
  padding: 10px 24px;
  font-weight: 500;
}
</style>