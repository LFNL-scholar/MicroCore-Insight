import api, { handleApiError } from './request'

// 绑定设备
export const bindDevice = async (code, userId) => {
  try {
    console.log('Binding device with code:', code, 'for user:', userId)
    const response = await api.post('/api/frontend/device', {
      code: code,
      user_id: userId
    })
    
    console.log('Bind device response:', response.data)
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
      throw new Error('认证码错误，请检查后重试')
    }

    handleApiError(error, 'bindDevice')
  }
}
