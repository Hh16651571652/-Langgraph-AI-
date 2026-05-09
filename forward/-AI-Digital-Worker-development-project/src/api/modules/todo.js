// 代办事项API模块
import api from '../index.js'

/**
 * 获取代办事项列表
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export const getTodoList = (params = {}) => {
  return api.get('/todo/list', { params })
}

/**
 * 创建代办事项
 * @param {Object} data - 任务数据
 * @returns {Promise}
 */
export const createTodo = (data) => {
  return api.post('/todo/create', data)
}

/**
 * 更新任务状态
 * @param {number} id - 任务ID
 * @param {string} status - 新状态
 * @param {string} completionTime - 完成时间（可选）
 * @returns {Promise}
 */
export const updateTodoStatus = (id, status, completionTime = null) => {
  const data = { status }
  if (completionTime) {
    data.completionTime = completionTime
  }
  return api.put(`/todo/${id}/status`, data)
}

/**
 * 删除代办事项
 * @param {number} id - 任务ID
 * @returns {Promise}
 */
export const deleteTodo = (id) => {
  return api.delete(`/todo/${id}`)
}

/**
 * 获取代办统计信息
 * @returns {Promise}
 */
export const getTodoStats = () => {
  return api.get('/todo/stats')
}