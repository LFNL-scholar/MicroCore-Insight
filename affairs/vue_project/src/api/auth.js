import axios from 'axios'

// 使用相对路径，让 Vite 代理处理请求
const API_BASE_URL = ''

// 创建 axios 实例
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000, // 增加超时时间
  headers: {
    'Content-Type': 'application/json'
  }
})

// 添加请求拦截器
api.interceptors.request.use(
  config => {
    // 打印请求信息，便于调试
    console.log('Request:', {
      url: config.url,
      method: config.method,
      data: config.data
    })
    return config
  },
  error => {
    console.error('Request Error:', error)
    return Promise.reject(error)
  }
)

// 添加响应拦截器
api.interceptors.response.use(
  response => {
    console.log('Response:', response.data)
    return response
  },
  error => {
    console.error('Response Error:', {
      status: error.response?.status,
      data: error.response?.data,
      message: error.message
    })
    return Promise.reject(error)
  }
)

// 登录服务
export const login = async (userId, password) => {
  try {
    const response = await api.post('/api/auth/login', {
      user_id: userId,
      password: password
    })
    return response.data
  } catch (error) {
    handleApiError(error, 'login')
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
    handleApiError(error, 'register')
  }
}

// 删除用户服务
export const deleteUser = async (userId, password) => {
  try {
    const response = await api.delete('/api/auth/delete', {
      data: {
        user_id: userId,
        password: password
      }
    })
    return response.data
  } catch (error) {
    handleApiError(error, 'delete')
  }
}

// 统一的错误处理函数
const handleApiError = (error, operation) => {
  console.error(`${operation} error:`, {
    message: error.message,
    status: error.response?.status,
    data: error.response?.data
  })
  
  if (error.response) {
    // 服务器响应错误
    throw {
      status: error.response.status,
      message: error.response.data.detail || `${operation} 失败`
    }
  } else if (error.code === 'ERR_NETWORK') {
    // 网络错误
    throw {
      status: 0,
      message: '无法连接到服务器，请确保服务器已启动'
    }
  } else if (error.code === 'ECONNABORTED') {
    // 请求超时
    throw {
      status: 408,
      message: '请求超时，请稍后重试'
    }
  } else {
    // 其他错误
    throw {
      status: 500,
      message: `${operation} 失败: ${error.message || '未知错误'}`
    }
  }
}