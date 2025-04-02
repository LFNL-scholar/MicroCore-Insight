import axios from 'axios'

const API_BASE_URL = 'http://localhost:8005'

// 创建 axios 实例
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 登录服务
export const login = async (userId, password) => {
  try {
    const response = await api.post('/api/auth/login', {
      user_id: userId,
      password: password
    })
    return response.data
  } catch (error) {
    if (error.response) {
      // 服务器响应错误
      throw {
        status: error.response.status,
        message: error.response.data.detail
      }
    } else if (error.request) {
      // 请求发送失败
      throw {
        status: 0,
        message: '网络连接失败，请检查网络设置'
      }
    } else {
      // 其他错误
      throw {
        status: 500,
        message: '请求发送失败'
      }
    }
  }
}

// 注册服务
export const register = async (userId, password) => {
  try {
    const response = await api.post('/api/auth/register', {
      user_id: userId,
      password: password
    })
    return response.data
  } catch (error) {
    if (error.response) {
      // 服务器响应错误
      throw {
        status: error.response.status,
        message: error.response.data.detail
      }
    } else if (error.request) {
      // 请求发送失败
      throw {
        status: 0,
        message: '网络连接失败，请检查网络设置'
      }
    } else {
      // 其他错误
      throw {
        status: 500,
        message: '请求发送失败'
      }
    }
  }
} 