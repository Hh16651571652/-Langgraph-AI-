<template>
  <div class="app-container">
    <!-- 侧边栏导航 -->
    <div class="sidebar">
      <div class="logo-area">
        <h2>🤖 AI数字员工</h2>
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
      <div class="top-navbar">
        <!-- 全局自然语言输入栏 -->
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
        
        <!-- 用户信息区域 -->
        <div class="user-area-top">
          <div class="user-info-top">
            <div class="user-details-top">
              <div class="username-top">{{ userInfo.username || '用户' }}</div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 路由视图 -->
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox, ElLoading } from 'element-plus'
import { logout } from '@/api/modules/auth'
import { chatWithAgent } from '@/api/modules/agent'

const router = useRouter()
const nlpCommand = ref('')

// 用户信息
const userInfo = ref({
  username: '',
  loginTime: ''
})

// 获取菜单路由
const menuRoutes = computed(() => {
  const mainRoute = router.options.routes.find(route => route.path === '/')
  return mainRoute?.children || []
})

// 格式化登录时间
const formatLoginTime = (loginTime) => {
  if (!loginTime) return '未登录'
  
  const date = new Date(loginTime)
  return `登录于 ${date.toLocaleDateString()} ${date.toLocaleTimeString()}`
}

// 处理退出登录
const handleLogout = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要退出登录吗？',
      '退出确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 调用退出登录API
    await logout()
    
    // 清除本地存储
    localStorage.removeItem('userInfo')
    document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'
    
    ElMessage.success('退出登录成功')
    
    // 跳转到登录页
    router.push('/login')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('退出登录失败')
    }
  }
}

// 加载用户信息
const loadUserInfo = () => {
  const storedUserInfo = localStorage.getItem('userInfo')
  if (storedUserInfo) {
    userInfo.value = JSON.parse(storedUserInfo)
  }
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
    if (result.execution_result && result.execution_result.success) {
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
        // 聊天类型显示回复消息
        ElMessage.success({
          message: result.response || '✅ 请求已处理',
          duration: 3
        })
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
  loadUserInfo()
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

/* 顶部用户信息区域 */
.user-area-top {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-left: 24px;
  min-width: 200px;
  justify-content: flex-end;
}

.user-info-top {
  display: flex;
  align-items: center;
  padding: 8px 16px;
  background: #f8f9fa;
  border-radius: 20px;
  border: 1px solid #eef2ff;
}

.user-details-top {
  display: flex;
  flex-direction: column;
  gap: 2px;
  align-items: center;
}

.username-top {
  font-weight: 600;
  color: #374151;
  font-size: 0.85rem;
}

.login-time-top {
  font-size: 0.7rem;
  color: #6b7280;
}

.logout-btn-top {
  color: #6b7280 !important;
  font-size: 0.8rem;
  padding: 6px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
}

.logout-btn-top:hover {
  color: #ef4444 !important;
  border-color: #ef4444;
  background: #fef2f2 !important;
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