<template>
  <div class="app-container">
    <!-- 侧边栏导航 -->
    <div class="sidebar">
      <div class="logo-area">
        <!-- ✅ 用户账户按钮（替代原来的"AI数字员工"） -->
        <div class="user-account-btn" @click="showUserDialog = true">
          <div class="user-avatar">{{ userAvatar }}</div>
          <div class="user-info">
            <span class="user-id">{{ currentUsername }}</span>
            <span class="user-status">在线</span>
          </div>
        </div>
        <p>智能协同 · 敏捷办公</p>
      </div>
      <div class="nav-menu">
        <div 
          v-for="route in menuRoutes" 
          :key="route.path"
          class="nav-item" 
          :class="{ active: $route.path === '/' + route.path }"
          @click="$router.push('/' + route.path)"
        >
          <i>{{ route.meta.icon }}</i>
          <span>{{ route.meta.title }}</span>
        </div>
      </div>
      
      <div style="padding: 20px; font-size: 12px; color: #8aa9cc; text-align: center;">
        本地化部署 | 安全可控
      </div>
    </div>

    <!-- 右侧主内容 -->
    <div class="main-content">
      <!-- 顶部导航栏 -->
      <div class="top-navbar" v-if="$route.path !== '/chat'">
        <!-- 全局自然语言输入栏（Chat页面不显示） -->
        <div class="nlp-bar">
          <i>💬</i>
          <input 
            type="text" 
            v-model="nlpCommand" 
            placeholder="跟我说一句话，例如：帮我预定明天下午2点的会议室，并提醒我写周报..." 
            @keyup.enter="handleNlpCommand"
          >
          <button @click="handleNlpCommand">发送指令</button>
        </div>
      </div>
      
      <!-- 路由视图 -->
      <router-view />
    </div>
    
    <!-- 任务选择对话框 -->
    <el-dialog
      v-model="showTodoSelectDialog"
      title="📋 请选择要完成的任务"
      width="600px"
      :close-on-click-modal="false"
    >
      <div class="todo-select-list">
        <el-table
          :data="todoCandidates"
          style="width: 100%"
          highlight-current-row
          @current-change="handleTodoSelect"
        >
          <el-table-column label="选择" width="80">
            <template #default="scope">
              <el-radio
                v-model="selectedTodoId"
                :label="scope.row.id"
              >
                &nbsp;
              </el-radio>
            </template>
          </el-table-column>
          <el-table-column prop="title" label="任务标题" min-width="150" />
          <el-table-column prop="due_date" label="截止时间" width="160">
            <template #default="scope">
              {{ formatDueDate(scope.row.due_date) }}
            </template>
          </el-table-column>
          <el-table-column prop="priority" label="优先级" width="100">
            <template #default="scope">
              <el-tag :type="getPriorityType(scope.row.priority)" size="small">
                {{ getPriorityText(scope.row.priority) }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="cancelTodoSelect">取消</el-button>
          <el-button type="primary" @click="confirmTodoComplete" :disabled="!selectedTodoId">
            确认完成
          </el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- ✅ 用户信息弹窗 -->
    <el-dialog
      v-model="showUserDialog"
      title="👤 用户信息"
      width="500px"
      :close-on-click-modal="false"
      class="user-info-dialog"
    >
      <div class="user-profile">
        <!-- 头像区域 -->
        <div class="profile-header">
          <div class="profile-avatar-large">{{ userAvatar }}</div>
          <div class="profile-name">{{ currentUsername }}</div>
          <el-tag type="success" size="small">在线</el-tag>
        </div>
        
        <!-- 用户详细信息 -->
        <div class="profile-details">
          <div class="detail-item">
            <span class="detail-label">账号：</span>
            <span class="detail-value">{{ currentUsername }}</span>
          </div>
          
          <!-- ✅ 邮箱（可编辑） -->
          <div class="detail-item">
            <span class="detail-label">邮箱：</span>
            <div class="editable-field">
              <el-input
                v-if="isEditingEmail"
                v-model="editEmail"
                placeholder="请输入邮箱地址"
                size="small"
                style="width: 100%;"
                @blur="saveEmail"
                @keyup.enter="saveEmail"
              />
              <div v-else class="field-display" @click="startEditEmail">
                <span class="field-value">{{ currentUserEmail || '未设置' }}</span>
                <el-icon class="edit-icon"><Edit /></el-icon>
              </div>
            </div>
          </div>
          
          <!-- ✅ 个人标签（可编辑） -->
          <div class="detail-item">
            <span class="detail-label">个人标签：</span>
            <div class="editable-field">
              <el-input
                v-if="isEditingTag"
                v-model="editTag"
                placeholder="请输入个人标签"
                size="small"
                style="width: 100%;"
                @blur="saveTag"
                @keyup.enter="saveTag"
              />
              <div v-else class="field-display" @click="startEditTag">
                <div class="tags-container">
                  <el-tag v-for="tag in userTags" :key="tag" size="small" style="margin-right: 8px;">
                    {{ tag }}
                  </el-tag>
                  <span v-if="!userTags || userTags.length === 0" class="no-tags">暂无标签</span>
                </div>
                <el-icon class="edit-icon"><Edit /></el-icon>
              </div>
            </div>
          </div>
          
          <div class="detail-item">
            <span class="detail-label">加入时间：</span>
            <span class="detail-value">{{ formatDate(joinDate) }}</span>
          </div>
        </div>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button type="danger" @click="handleLogout" plain>
            <el-icon><SwitchButton /></el-icon>
            退出登录
          </el-button>
          <el-button type="primary" @click="showUserDialog = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox, ElLoading } from 'element-plus'
import { SwitchButton, Edit } from '@element-plus/icons-vue'
import { chatWithAgent } from '@/api/modules/agent'
import { getCurrentUser, logout as apiLogout, updateUserInfo } from '@/api/modules/auth'

const router = useRouter()
const nlpCommand = ref('')

// ✅ 用户相关状态
const showUserDialog = ref(false)
const currentUsername = ref(localStorage.getItem('username') || '用户')
const currentUserEmail = ref('')
const userTags = ref([])
const joinDate = ref(null)

// ✅ 编辑状态
const isEditingEmail = ref(false)
const editEmail = ref('')
const isEditingTag = ref(false)
const editTag = ref('')

// 任务选择对话框相关
const showTodoSelectDialog = ref(false)
const todoCandidates = ref([])
const selectedTodoId = ref(null)

// 获取菜单路由
const menuRoutes = computed(() => {
  const mainRoute = router.options.routes.find(route => route.path === '/')
  return mainRoute?.children || []
})

// ✅ 计算用户头像（取用户名首字母）
const userAvatar = computed(() => {
  const name = currentUsername.value
  if (!name) return 'U'
  // 如果是中文，取第一个字；如果是英文，取第一个字母并大写
  const firstChar = name.charAt(0)
  return /\u4e00-\u9fa5/.test(firstChar) ? firstChar : firstChar.toUpperCase()
})

// ✅ 获取当前用户信息
const fetchUserInfo = async () => {
  try {
    const userInfo = await getCurrentUser()
    if (userInfo) {
      currentUsername.value = userInfo.username || localStorage.getItem('username') || '用户'
      currentUserEmail.value = userInfo.email || ''
      // ✅ 使用 description 字段作为个人标签（如果是字符串，转换为数组）
      const desc = userInfo.description || ''
      userTags.value = desc ? [desc] : []
      joinDate.value = userInfo.created_at || null
      
      console.log('[用户信息] 从数据库获取:', {
        username: currentUsername.value,
        email: currentUserEmail.value,
        description: desc,
        tags: userTags.value,
        created_at: joinDate.value
      })
      
      // 更新localStorage
      localStorage.setItem('username', currentUsername.value)
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
    // 如果API调用失败，使用localStorage中的数据
    currentUsername.value = localStorage.getItem('username') || '用户'
  }
}

// ✅ 退出登录
const handleLogout = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要退出登录吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 调用登出API
    await apiLogout()
    
    // 清除本地存储
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    
    ElMessage.success('已退出登录')
    
    // 跳转到登录页
    router.push('/login')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('退出登录失败:', error)
      ElMessage.error('退出登录失败，请重试')
    }
  }
}

// ✅ 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '未知'
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// ✅ 邮箱编辑相关方法
const startEditEmail = () => {
  editEmail.value = currentUserEmail.value
  isEditingEmail.value = true
}

const saveEmail = async () => {
  // 如果为空，直接保存
  if (!editEmail.value || editEmail.value.trim() === '') {
    try {
      await updateUserInfo({ email: '' })
      currentUserEmail.value = ''
      ElMessage.success('邮箱已清空')
    } catch (error) {
      console.error('更新邮箱失败:', error)
      ElMessage.error('更新失败，请重试')
    } finally {
      isEditingEmail.value = false
    }
    return
  }
  
  // 验证邮箱格式
  const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
  if (!emailPattern.test(editEmail.value)) {
    ElMessage.error('邮箱格式不正确')
    return
  }
  
  try {
    await updateUserInfo({ email: editEmail.value })
    currentUserEmail.value = editEmail.value
    ElMessage.success('邮箱更新成功')
  } catch (error) {
    console.error('更新邮箱失败:', error)
    ElMessage.error(error.response?.data?.detail || '更新失败，请重试')
  } finally {
    isEditingEmail.value = false
  }
}

// ✅ 个人标签编辑相关方法
const startEditTag = () => {
  editTag.value = userTags.value.length > 0 ? userTags.value[0] : ''
  isEditingTag.value = true
}

const saveTag = async () => {
  const tagValue = editTag.value.trim()
  
  try {
    await updateUserInfo({ description: tagValue })
    userTags.value = tagValue ? [tagValue] : []
    ElMessage.success(tagValue ? '标签更新成功' : '标签已清空')
  } catch (error) {
    console.error('更新标签失败:', error)
    ElMessage.error('更新失败，请重试')
  } finally {
    isEditingTag.value = false
  }
}

// 任务选择对话框相关方法
const handleTodoSelect = (row) => {
  if (row) {
    selectedTodoId.value = row.id
  }
}

const cancelTodoSelect = () => {
  showTodoSelectDialog.value = false
  todoCandidates.value = []
  selectedTodoId.value = null
}

const formatDueDate = (dueDate) => {
  if (!dueDate) return '无'
  const date = new Date(dueDate)
  return date.toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getPriorityType = (priority) => {
  const types = {
    high: 'danger',
    medium: 'warning',
    low: 'info'
  }
  return types[priority] || 'info'
}

const getPriorityText = (priority) => {
  const texts = {
    high: '高',
    medium: '中',
    low: '低'
  }
  return texts[priority] || priority
}

const confirmTodoComplete = async () => {
  if (!selectedTodoId.value) return

  try {
    // 调用 API 完成任务
    const { updateTodoStatus } = await import('@/api/modules/todo')
    const completionTime = new Date().toISOString()
    
    await updateTodoStatus(selectedTodoId.value, 'completed', completionTime)
    
    ElMessage.success('任务已标记为完成！')
    
    // 关闭对话框
    showTodoSelectDialog.value = false
    todoCandidates.value = []
    selectedTodoId.value = null
    
    // 刷新当前页面数据（如果在 Todo 页面）
    if (router.currentRoute.value.path === '/todo') {
      router.push({ path: '/todo', query: { refresh: true, t: Date.now() } })
    }
  } catch (error) {
    console.error('完成任务失败:', error)
    ElMessage.error('完成任务失败，请重试')
  }
}

// 监听自定义事件
const handleShowTodoSelectDialog = (event) => {
  const { candidates, message } = event.detail
  todoCandidates.value = candidates || []
  selectedTodoId.value = null
  showTodoSelectDialog.value = true
}

// 自然语言指令处理
const handleNlpCommand = async () => {
  const cmd = nlpCommand.value.trim()
  if (!cmd) {
    console.log('[NLP] 输入为空')
    return
  }

  console.log('[NLP] 发送指令:', cmd)

  let loadingInstance = null
  try {
    loadingInstance = ElLoading.service({
      lock: true,
      text: '正在处理您的请求...',
      background: 'rgba(0, 0, 0, 0.7)'
    })

    // 调用AI agent API
    console.log('[NLP] 调用chatWithAgent...')
    const result = await chatWithAgent(cmd)
    console.log('[NLP] 收到响应:', result)

    loadingInstance.close()

    // 根据执行结果和任务类型显示对应消息和跳转
    if (result.execution_result && result.execution_result.action === 'select_todo') {
      // 需要用户选择任务 - 存储到 sessionStorage 并触发事件
      sessionStorage.setItem('todo_candidates', JSON.stringify(result.execution_result.candidates || []))
      
      // 触发自定义事件，通知当前页面显示对话框
      window.dispatchEvent(new CustomEvent('showTodoSelectDialog', {
        detail: {
          candidates: result.execution_result.candidates,
          message: result.response
        }
      }))
      
      // 清空输入
      nlpCommand.value = ''
      return
    } else if (result.execution_result && result.execution_result.success) {
      // 操作成功
      if (result.task_type === 'todo') {
        ElMessage.success({
          message: `✅ ${result.execution_result.message}`,
          duration: 2
        })
        // 导航到todo页面，并传递刷新标志
        router.push({ path: '/todo', query: { refresh: true } })
      } else if (result.task_type === 'meeting') {
        ElMessage.success({
          message: `✅ ${result.execution_result.message}`,
          duration: 2
        })
        
        // 如果有推荐的会议室或匹配的预约，存储到sessionStorage
        const meetingData = {
          recommended_rooms: result.execution_result.recommended_rooms || [],
          matched_bookings: result.execution_result.matched_bookings || []
        }
        sessionStorage.setItem('nlp_meeting_data', JSON.stringify(meetingData))
        
        router.push({ path: '/meeting', query: { refresh: true } })
      } else if (result.task_type === 'weather') {
        // 检查是否执行成功
        if (result.execution_result && result.execution_result.success === false) {
          // 日期校验失败等情况，显示错误消息但不跳转
          ElMessage.error({
            message: result.response || '❌ 天气查询失败',
            duration: 3
          })
        } else {
          // 执行成功，显示消息并跳转
          ElMessage.success({
            message: `✅ ${result.response}`,
            duration: 3
          })
          
          // 存储天气数据到sessionStorage
          const weatherData = {
            data: result.execution_result.data || {}
          }
          sessionStorage.setItem('nlp_weather_data', JSON.stringify(weatherData))
          
          router.push('/weather')
        }
      } else if (result.task_type === 'chat') {
        // 聊天类型：存储消息并跳转到chat页面
        const chatData = {
          userMessage: cmd,
          aiResponse: result.response,
          session_id: result.session_id,
          timestamp: new Date().toISOString(),
          task_type: result.task_type,
          execution_result: result.execution_result
        }
        sessionStorage.setItem('nlp_chat_message', JSON.stringify(chatData))
        
        ElMessage.success({
          message: '正在为您打开智能对话...',
          duration: 1.5
        })
        
        router.push('/chat')
      }
    } else if (result.execution_result) {
      // 操作失败
      ElMessage.error({
        message: `❌ ${result.execution_result.message}`,
        duration: 2
      })
      
      // 仍然跳转到对应页面
      if (result.task_type === 'todo') {
        router.push('/todo')
      } else if (result.task_type === 'meeting') {
        // 即使失败也传递数据（可能是需要确认的取消/完成操作）
        const meetingData = {
          recommended_rooms: result.execution_result.recommended_rooms || [],
          matched_bookings: result.execution_result.matched_bookings || []
        }
        sessionStorage.setItem('nlp_meeting_data', JSON.stringify(meetingData))
        router.push('/meeting')
      }
    } else {
      // 其他情况
      ElMessage.info({
        message: result.response || '✅ 请求已处理',
        duration: 2
      })
    }

    // 清空输入
    nlpCommand.value = ''

  } catch (error) {
    if (loadingInstance) {
      loadingInstance.close()
    }
    console.error('NLP指令处理失败:', error)
    ElMessage.error({
      message: '❌ 指令处理失败，请检查您的输入或稍后重试',
      duration: 3
    })
  }
}

onMounted(() => {
  // 监听任务选择对话框事件
  window.addEventListener('showTodoSelectDialog', handleShowTodoSelectDialog)
  
  // ✅ 获取用户信息
  fetchUserInfo()
})
</script>

<style scoped>
.app-container {
  display: flex;
  min-height: 100vh;
  background: #eef5ff;
}

/* 侧边栏样式 */
.sidebar {
  width: 260px;
  background: white;
  backdrop-filter: blur(4px);
  box-shadow: 2px 0 12px rgba(0, 80, 200, 0.05);
  display: flex;
  flex-direction: column;
  border-right: 1px solid #e2edff;
  transition: all 0.2s;
}

.logo-area {
  padding: 28px 20px;
  border-bottom: 1px solid #e9f0ff;
  margin-bottom: 20px;
}

/* ✅ 用户账户按钮样式 */
.user-account-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: linear-gradient(135deg, #eef4ff, #e0edfe);
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid transparent;
  margin-bottom: 12px;
}

.user-account-btn:hover {
  background: linear-gradient(135deg, #e0edfe, #d0e0fd);
  border-color: var(--primary);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(43, 110, 240, 0.15);
}

.user-avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  font-weight: 600;
  flex-shrink: 0;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
  min-width: 0;
}

.user-id {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-status {
  font-size: 0.75rem;
  color: #67c23a;
  display: flex;
  align-items: center;
  gap: 4px;
}

.user-status::before {
  content: '';
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #67c23a;
  display: inline-block;
}

.logo-area h2 {
  color: var(--primary);
  font-weight: 600;
  font-size: 1.5rem;
  letter-spacing: 1px;
}

.logo-area p {
  font-size: 0.75rem;
  color: #6c8db0;
  margin-top: 6px;
}

.nav-menu {
  flex: 1;
  padding: 0 16px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  margin-bottom: 8px;
  border-radius: 14px;
  cursor: pointer;
  color: #2c4e7a;
  transition: all 0.2s;
  font-weight: 500;
}

.nav-item i {
  font-size: 1.3rem;
  width: 24px;
  text-align: center;
}

.nav-item.active {
  background: linear-gradient(135deg, #eef4ff, #e0edfe);
  color: var(--primary);
  font-weight: 600;
  box-shadow: 0 2px 6px rgba(43, 110, 240, 0.1);
  border-left: 3px solid var(--primary);
}

.nav-item:hover:not(.active) {
  background: #f4f9ff;
  color: var(--primary);
}

/* 顶部导航栏 */
.top-navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 0 0 16px 0;
  border-bottom: 1px solid var(--border-light);
}

/* 主内容区 */
.main-content {
  flex: 1;
  padding: 24px 32px;
  overflow-y: auto;
}

/* Chat页面特殊样式 - 减少顶部padding */
.main-content:has(.chat-page) {
  padding-top: 8px;
}

/* 顶部自然语言交互条 */
.nlp-bar {
  background: white;
  border-radius: 60px;
  padding: 8px 20px;
  box-shadow: var(--shadow-sm);
  display: flex;
  align-items: center;
  flex: 1;
  max-width: none;
  gap: 12px;
  margin-bottom: 0;
  border: 1px solid #cde2ff;
}

.nlp-bar i {
  font-size: 1.6rem;
  color: var(--primary);
}

.nlp-bar input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 1rem;
  padding: 12px 0;
  background: transparent;
}

.nlp-bar button {
  background: var(--primary);
  border: none;
  color: white;
  border-radius: 40px;
  padding: 8px 24px;
  cursor: pointer;
  transition: 0.2s;
}

.nlp-bar button:hover {
  background: var(--primary-dark);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .sidebar { width: 80px; }
  .logo-area h2, .logo-area p, .nav-item span:last-child { display: none; }
  .nav-item { justify-content: center; }
  .main-content { padding: 16px; }
  
  /* ✅ 移动端适配用户按钮 */
  .user-account-btn {
    padding: 8px;
    justify-content: center;
  }
  
  .user-info {
    display: none;
  }
}

/* ✅ 用户信息弹窗样式 */
.user-info-dialog :deep(.el-dialog__body) {
  padding: 24px;
}

.user-profile {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.profile-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding-bottom: 20px;
  border-bottom: 2px solid #e9f0ff;
}

.profile-avatar-large {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(43, 110, 240, 0.2);
}

.profile-name {
  font-size: 1.3rem;
  font-weight: 600;
  color: #303133;
}

.profile-details {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.detail-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  background: #f8fafc;
  border-radius: 8px;
  transition: all 0.2s;
}

.detail-item:hover {
  background: #eef4ff;
}

.detail-label {
  font-size: 0.9rem;
  color: #606266;
  font-weight: 500;
  min-width: 80px;
  flex-shrink: 0;
}

.detail-value {
  font-size: 0.9rem;
  color: #303133;
  flex: 1;
  word-break: break-all;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  flex: 1;
}

.no-tags {
  font-size: 0.85rem;
  color: #909399;
  font-style: italic;
}

/* ✅ 可编辑字段样式 */
.editable-field {
  flex: 1;
}

.field-display {
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: all 0.2s;
}

.field-display:hover {
  background: #eef4ff;
}

.field-value {
  flex: 1;
  color: #303133;
}

.edit-icon {
  color: var(--primary);
  font-size: 14px;
  opacity: 0;
  transition: opacity 0.2s;
}

.field-display:hover .edit-icon {
  opacity: 1;
}
</style>

<style>
/* 全局样式变量 */
:root {
  --primary-light: #5c9eff;
  --primary: #2b6ef0;
  --primary-dark: #0a58ca;
  --bg-sidebar: #ffffffd9;
  --bg-card: #ffffff;
  --shadow-sm: 0 4px 12px rgba(0, 82, 212, 0.08);
  --border-light: #d9e8ff;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', 'PingFang SC', Roboto, 'Helvetica Neue', sans-serif;
  background-color: #eef5ff;
  overflow-x: hidden;
}
</style>