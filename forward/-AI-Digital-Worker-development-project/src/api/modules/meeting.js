// 会议室管理API模块
import api from '../index.js'

/**
 * 获取会议室列表
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export const getMeetingRooms = (params = {}) => {
  return api.get('/meeting/rooms', { params })
}

/**
 * 获取会议室预约记录
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export const getMyBookings = (params = {}) => {
  return api.get('/meeting/bookings/my', { params })
}

/**
 * 快速预定会议室
 * @param {number} roomId - 会议室ID
 * @param {Object} bookingData - 预定数据
 * @returns {Promise}
 */
export const quickBookRoom = (roomId, bookingData) => {
  return api.post(`/meeting/rooms/${roomId}/book`, bookingData)
}

/**
 * 取消预约
 * @param {number} bookingId - 预约ID
 * @returns {Promise}
 */
export const cancelBooking = (bookingId) => {
  return api.delete(`/meeting/bookings/${bookingId}`)
}

/**
 * 完成预约
 * @param {number} bookingId - 预约ID
 * @returns {Promise}
 */
export const completeBooking = (bookingId) => {
  return api.put(`/meeting/bookings/${bookingId}/complete`)
}

/**
 * 获取会议室使用统计
 * @param {Object} params - 统计参数
 * @returns {Promise}
 */
export const getMeetingStats = (params = {}) => {
  return api.get('/meeting/stats', { params })
}

/**
 * 自然语言预定会议室
 * @param {string} command - 自然语言指令
 * @returns {Promise}
 */
export const nlpBookMeeting = (command) => {
  return api.post('/meeting/nlp-book', { command })
}

/**
 * NLP智能命令处理(预订/取消/完成)
 * @param {string} text - 自然语言指令
 * @returns {Promise}
 */
export const nlpCommand = (text) => {
  return api.post('/meeting/nlp-command', { text })
}