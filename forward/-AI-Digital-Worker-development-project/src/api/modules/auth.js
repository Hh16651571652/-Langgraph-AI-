// 认证相关API模块
import api from '../index.js'

/**
 * 用户登录
 * @param {Object} data - 登录数据
 * @param {string} data.username - 用户名
 * @param {string} data.password - 密码
 * @returns {Promise}
 */
export const login = (data) => {
  return api.post('/auth/login', data)
}

/**
 * 用户注册
 * @param {Object} data - 注册数据
 * @param {string} data.username - 用户名
 * @param {string} data.password - 密码
 * @returns {Promise}
 */
export const register = (data) => {
  return api.post('/auth/register', data)
}

/**
 * 用户登出
 * @returns {Promise}
 */
export const logout = () => {
  return api.post('/auth/logout')
}

/**
 * 获取当前用户信息
 * @returns {Promise}
 */
export const getCurrentUser = () => {
  return api.get('/auth/me')
}

/**
 * 验证token是否有效
 * @returns {Promise}
 */
export const verifyToken = () => {
  return api.get('/auth/verify')
}

/**
 * 刷新token
 * @returns {Promise}
 */
export const refreshToken = () => {
  return api.post('/auth/refresh')
}

/**
 * 更新当前用户信息
 * @param {Object} data - 更新数据
 * @param {string} data.email - 邮箱地址（可选）
 * @param {string} data.description - 个人描述/标签（可选）
 * @returns {Promise}
 */
export const updateUserInfo = (data) => {
  return api.put('/auth/me', data)
}