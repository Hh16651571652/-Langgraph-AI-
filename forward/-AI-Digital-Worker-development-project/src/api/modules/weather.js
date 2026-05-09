// 天气服务API模块
import api from '../index.js'

/**
 * 获取完整天气信息（当前+7天预报+24小时预报）
 * 这是天气查询的唯一入口
 * 
 * @param {string} city - 城市名称
 * @param {string} date - 查询日期（今天/明天/后天/YYYY-MM-DD）
 * @returns {Promise}
 */
export const getAllWeather = (city, date = '今天') => {
  return api.get('/weather/all', { params: { city, date } })
}

// 注意：以下旧接口已废弃，统一使用 getAllWeather
// export const getCurrentWeather = (city) => { ... }
// export const getWeatherForecast = (city, days) => { ... }
// export const getWeatherSuggestion = (city) => { ... }
// export const getHourlyForecast = (city) => { ... }
