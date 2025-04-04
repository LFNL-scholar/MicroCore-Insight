import axios from 'axios'

// 创建 axios 实例
const api = axios.create({
  baseURL: '',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 添加请求拦截器
api.interceptors.request.use(
  config => {
    console.log('Request:', {
      url: config.url,
      method: config.method,
      params: config.params,
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

// 统一的错误处理函数
export const handleApiError = (error, operation) => {
  console.error(`${operation} error:`, {
    message: error.message,
    status: error.response?.status,
    data: error.response?.data
  })
  
  if (error.response) {
    // 服务器响应错误
    if (error.response.status === 405) {
      throw {
        status: 405,
        message: '请求方法不允许，请联系技术支持'
      }
    }
    throw {
      status: error.response.status,
      message: error.response.data?.detail || `${operation}失败: ${error.response.statusText}`
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
      message: `${operation}失败: ${error.message || '未知错误'}`
    }
  }
}

export default api 