<template>
  <div class="login-container">
    <!-- 左侧背景区域 -->
    <div class="login-background">
      <div class="background-overlay">
        <div class="background-content">
          <h1>🤖 AI数字员工系统</h1>
          <p>智能协同 · 敏捷办公 · 未来已来</p>
          <div class="feature-list">
            <div class="feature-item">
              <span class="feature-icon">📋</span>
              <span>智能待办管理</span>
            </div>
            <div class="feature-item">
              <span class="feature-icon">📅</span>
              <span>会议室预约</span>
            </div>
            <div class="feature-item">
              <span class="feature-icon">🌤️</span>
              <span>天气助手</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 右侧登录区域 -->
    <div class="login-sidebar">
      <div class="login-card">
        <div class="login-header">
          <h2>🤖 AI数字员工系统</h2>
          <p class="login-subtitle">智能登录 · 安全访问</p>
        </div>
        
        <el-form 
          ref="loginFormRef" 
          :model="loginForm" 
          :rules="loginRules" 
          class="login-form"
          @submit.prevent="handleLogin"
        >
          <el-form-item prop="username" label="用户名">
            <el-input
              v-model="loginForm.username"
              placeholder="请输入用户名"
              size="large"
            />
          </el-form-item>
          
          <el-form-item prop="password" label="密码">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              size="large"
              show-password
              @keyup.enter="handleLogin"
              style="margin-left: 4px;"
            />
          </el-form-item>
          
          <el-form-item>
            <el-button 
              type="primary" 
              size="large" 
              class="login-btn"
              :loading="loading"
              @click="handleLogin"
            >
              {{ loading ? '登录中...' : '登录' }}
            </el-button>
          </el-form-item>
        </el-form>
        
        <div class="login-footer">
          <p>还没有账号？<span class="register-link" @click="showRegisterDialog = true">立即注册</span></p>
        </div>
      </div>
    </div>
    
    <!-- 注册对话框 -->
    <el-dialog
      v-model="showRegisterDialog"
      title="用户注册"
      width="400px"
      :close-on-click-modal="false"
    >
      <el-form 
        ref="registerFormRef" 
        :model="registerForm" 
        :rules="registerRules"
        label-width="80px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="registerForm.username" placeholder="请输入用户名" />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input v-model="registerForm.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="registerForm.confirmPassword" type="password" placeholder="请再次输入密码" show-password />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showRegisterDialog = false">取消</el-button>
          <el-button type="primary" @click="handleRegister" :loading="registerLoading">
            {{ registerLoading ? '注册中...' : '注册' }}
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { login, register } from '@/api/modules/auth'

const router = useRouter()
const loginFormRef = ref()
const registerFormRef = ref()
const loading = ref(false)
const showRegisterDialog = ref(false)
const registerLoading = ref(false)

// 登录表单数据
const loginForm = reactive({
  username: '',
  password: ''
})

// 表单验证规则
const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ]
}

// 注册表单数据
const registerForm = reactive({
  username: '',
  password: '',
  confirmPassword: ''
})

// 注册表单验证规则
const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== registerForm.password) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 处理登录
const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    const valid = await loginFormRef.value.validate()
    if (!valid) return
    
    loading.value = true
    
    // 调用真实登录API
    const response = await login(loginForm)
    
    // 存储token到localStorage和cookie
    if (response.token) {
      document.cookie = `token=${response.token}; path=/; max-age=604800` // 7天
      localStorage.setItem('token', response.token)
      
      // 存储用户信息到localStorage
      localStorage.setItem('userInfo', JSON.stringify({
        username: loginForm.username,
        loginTime: new Date().toISOString()
      }))
      
      ElMessage.success('登录成功！')
      
      // 跳转到首页
      router.push('/')
    }
  } catch (error) {
    ElMessage.error('登录失败：' + (error.response?.data?.detail || error.message || '用户名或密码错误'))
  } finally {
    loading.value = false
  }
}

// 处理注册
const handleRegister = async () => {
  if (!registerFormRef.value) return
  
  try {
    const valid = await registerFormRef.value.validate()
    if (!valid) return
    
    registerLoading.value = true
    
    // 调用注册API
    await register({
      username: registerForm.username,
      password: registerForm.password
    })
    
    ElMessage.success('注册成功！请登录')
    showRegisterDialog.value = false
    
    // 清空表单
    registerForm.username = ''
    registerForm.password = ''
    registerForm.confirmPassword = ''
    
  } catch (error) {
    ElMessage.error('注册失败：' + (error.message || '未知错误'))
  } finally {
    registerLoading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  position: relative;
  overflow: hidden;
}

/* 左侧背景区域 */
.login-background {
  flex: 1;
  background: 
    linear-gradient(135deg, rgba(43, 110, 240, 0.9) 0%, rgba(16, 185, 129, 0.7) 100%),
    url('https://images.unsplash.com/photo-1635070041078-e363dbe005cb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80');
  background-size: cover;
  background-position: center;
  background-blend-mode: overlay;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.background-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 30% 70%, rgba(43, 110, 240, 0.4) 0%, transparent 60%),
    radial-gradient(circle at 70% 30%, rgba(30, 130, 230, 0.3) 0%, transparent 60%),
    radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.15) 0%, transparent 70%);
  animation: float 12s ease-in-out infinite;
}

.background-content {
  position: relative;
  z-index: 10;
  color: white;
  text-align: center;
  max-width: 500px;
  padding: 0 40px;
}

.background-content h1 {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 16px;
  text-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  background: linear-gradient(135deg, #ffffff, #e0f7fa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.background-content p {
  font-size: 1.2rem;
  margin-bottom: 40px;
  opacity: 0.9;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.feature-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: flex-start;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.1rem;
  opacity: 0.9;
  transition: all 0.3s ease;
}

.feature-item:hover {
  opacity: 1;
  transform: translateX(5px);
}

.feature-icon {
  font-size: 1.4rem;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  padding: 8px;
  backdrop-filter: blur(10px);
}

/* 右侧登录区域 */
.login-sidebar {
  width: 480px;
  background: 
    linear-gradient(135deg, rgba(240, 245, 255, 0.95) 0%, rgba(230, 240, 255, 0.98) 100%),
    url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="blue-pattern" x="0" y="0" width="60" height="60" patternUnits="userSpaceOnUse"><circle cx="30" cy="30" r="1" fill="rgba(43, 110, 240, 0.05)"/><circle cx="45" cy="15" r="0.8" fill="rgba(30, 130, 230, 0.03)"/><circle cx="15" cy="45" r="0.5" fill="rgba(43, 110, 240, 0.02)"/></pattern></defs><rect width="100" height="100" fill="url(%23blue-pattern)"/></svg>');
  backdrop-filter: blur(15px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  position: relative;
  box-shadow: -4px 0 40px rgba(43, 110, 240, 0.15);
}

.login-sidebar::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 1px;
  background: linear-gradient(to bottom, transparent, rgba(43, 110, 240, 0.4), transparent);
}

@keyframes float {
  0%, 100% { 
    transform: translateY(10px) rotate(0deg) scale(1); 
    opacity: 0.8;
  }
  33% { 
    transform: translateY(-10px) rotate(1deg) scale(1.02); 
    opacity: 1;
  }
  66% { 
    transform: translateY(5px) rotate(-0.5deg) scale(0.98); 
    opacity: 0.9;
  }
}

.login-card {
  width: 100%;
  max-width: 380px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  border: 1px solid rgba(255, 255, 255, 0.5);
  animation: cardAppear 0.6s ease-out;
}

@keyframes cardAppear {
  0% {
    opacity: 0;
    transform: translateX(20px) scale(0.95);
  }
  100% {
    opacity: 1;
    transform: translateX(0) scale(1);
  }
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-header h2 {
  margin: 0 0 10px 0;
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
  background: linear-gradient(135deg, #2b6ef0, #10b981);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.5px;
}

.login-header p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.login-form {
  margin-bottom: 24px;
}

/* 调整表单项样式 */
.login-form .el-form-item {
  margin-bottom: 24px;
  display: flex;
  align-items: center;
}

.login-form .el-form-item__label {
  font-weight: 500;
  color: var(--text-primary);
  width: 80px;
  text-align: right;
  margin-right: 12px;
  margin-bottom: 0;
}

.login-form .el-form-item__content {
  flex: 1;
  display: flex;
}

.login-form .el-input {
  width: 100%;
}

.login-form .el-input__wrapper {
  border-radius: 8px;
  padding: 0 12px;
  width: 100%;
}

.login-form .el-input__inner {
  padding: 8px 0;
  width: 100%;
}

.login-btn {
  width: 100%;
  background: linear-gradient(135deg, #2b6ef0, #1a4bd6);
  border: none;
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: 1rem;
  letter-spacing: 1px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  padding: 14px 24px;
  box-shadow: 
    0 4px 15px rgba(43, 110, 240, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.login-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.6s;
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 8px 25px rgba(43, 110, 240, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.login-btn:hover::before {
  left: 100%;
}

.login-btn:active {
  transform: translateY(0);
  box-shadow: 
    0 2px 8px rgba(43, 110, 240, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.login-footer {
  text-align: center;
  border-top: 1px solid var(--border-light);
  padding-top: 16px;
}

.login-footer p {
  margin: 0;
  color: var(--text-tertiary);
  font-size: 0.8rem;
}

.register-link {
  color: #2b6ef0;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s;
}

.register-link:hover {
  color: #1e5dd0;
  text-decoration: underline;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .login-card {
    padding: 24px;
    margin: 0 16px;
  }
  
  .login-header h2 {
    font-size: 1.5rem;
  }
}
</style>