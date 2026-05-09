// 提醒功能API模块
import api from '../index.js'

/**
 * 获取即将逾期任务列表（分页查询）
 * @param {Object} params - 查询参数
 * @param {number} params.hours - 提前提醒时间（小时），默认1小时
 * @param {number} params.page - 当前页码
 * @param {number} params.page_size - 每页记录数
 * @returns {Promise}
 */
export const getUpcomingOverdueTasks = (params = {}) => {
  // 设置默认分页参数
  const defaultParams = {
    hours: 1.0,  // 默认1小时阈值
    page: 1,
    page_size: 5
  }
  
  return api.get('/todo/reminder/overdue-soon', { 
    params: { ...defaultParams, ...params }
  })
}

/**
 * 获取提醒统计信息
 * @returns {Promise}
 */
export const getReminderStats = () => {
  return api.get('/reminder/stats')
}

/**
 * 标记提醒为已读
 * @param {number} taskId - 任务ID
 * @returns {Promise}
 */
export const markReminderAsRead = (taskId) => {
  return api.put(`/reminder/tasks/${taskId}/read`)
}

/**
 * 获取提醒设置
 * @returns {Promise}
 */
export const getReminderSettings = () => {
  return api.get('/reminder/settings')
}

/**
 * 更新提醒设置
 * @param {Object} settings - 提醒设置
 * @returns {Promise}
 */
export const updateReminderSettings = (settings) => {
  return api.put('/reminder/settings', settings)
}