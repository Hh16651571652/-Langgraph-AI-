// API统一管理入口
import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 30000, // 🔥 默认超时 30s
  headers: {
    'Content-Type': 'application/json'
  }
})

// 🔥 针对不同接口设置不同的超时时间
const TIMEOUT_CONFIG = {
  '/agent/chat': 60000,      // LLM对话：60s
  '/weather': 15000,         // 天气查询：15s
  '/default': 30000          // 默认：30s
}

// 请求拦截器 - 动态设置超时
api.interceptors.request.use(
  config => {
    // 根据 URL 匹配超时时间
    let timeout = TIMEOUT_CONFIG['/default']
    for (const [path, time] of Object.entries(TIMEOUT_CONFIG)) {
      if (config.url.includes(path)) {
        timeout = time
        break
      }
    }
    config.timeout = timeout
    
    // 添加认证token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    // 统一处理响应格式
    // 支持200(成功)和201(创建成功)
    if (response.data && (response.data.code === 200 || response.data.code === 201)) {
      return response.data.data
    }
    return Promise.reject(new Error(response.data?.message || '请求失败'))
  },
  error => {
    // 统一错误处理
    if (error.response?.status === 401) {
      // token过期，跳转到登录页
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api