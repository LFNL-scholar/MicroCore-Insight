import api, { handleApiError } from './request'

// 获取用户设备列表
export const getUserDevices = async (userId) => {
  try {
    console.log('Fetching devices for user:', userId)
    const response = await api.get('/api/frontend/user/devices', {
      params: { user_id: userId }
    })
    
    console.log('Get user devices response:', response.data)
    return response.data
  } catch (error) {
    // 增加更详细的错误日志
    console.error('Get user devices error:', {
      method: 'GET',
      url: '/api/frontend/user/devices',
      params: { user_id: userId },
      error: {
        message: error.message,
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data
      }
    })

    if (error.response?.status === 404) {
      throw new Error('用户不存在')
    }

    handleApiError(error, 'getUserDevices')
  }
}

// 绑定设备
export const bindDevice = async (code, userId) => {
  try {
    console.log('Binding device with code:', code, 'for user:', userId)
    const response = await api.post('/api/frontend/device', {
      code: code,
      user_id: userId
    })
    
    console.log('Bind device response:', response.data)

    // 验证响应格式
    if (response.data.status !== 'success') {
      throw new Error(response.data.message || '设备绑定失败')
    }

    return response.data
  } catch (error) {
    // 增加更详细的错误日志
    console.error('Bind device error:', {
      method: 'POST',
      url: '/api/frontend/device',
      data: { code, user_id: userId },
      error: {
        message: error.message,
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data
      }
    })

    // 处理特定的错误状态
    if (error.response?.status === 401) {
      throw new Error(error.response.data.detail || '认证码错误')
    }

    if (error.response?.status === 500) {
      throw new Error(error.response.data.detail || '服务器内部错误，请稍后重试')
    }

    // 处理其他错误
    if (error.response?.data?.detail) {
      throw new Error(error.response.data.detail)
    }

    handleApiError(error, 'bindDevice')
  }
}
