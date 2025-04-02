import api, { handleApiError } from './request'

// 获取用户信息
export const getUserInfo = async (userId) => {
  try {
    console.log('Fetching user info for:', userId)
    const response = await api.get('/api/frontend/user/info', {
      params: { user_id: userId }
    })
    
    // 打印原始响应数据
    console.log('Raw user info response:', response.data)
    
    // 确保返回数据包含必要的字段
    const userData = response.data
    return {
      status: 'success',
      nickname: userData.nickname || '',
      email: userData.email || '',
      phone: userData.phone || '',
      ...userData
    }
  } catch (error) {
    handleApiError(error, 'getUserInfo')
  }
}

// 更新用户信息
export const updateUserInfo = async (userData) => {
  try {
    console.log('Updating user info:', userData)
    const response = await api.post('/api/frontend/user/update', userData)
    
    console.log('Update response:', response.data)
    return response.data
  } catch (error) {
    // 增加更详细的错误日志
    console.error('Update user info error:', {
      method: 'POST',
      url: '/api/frontend/user/update',
      data: userData,
      error: {
        message: error.message,
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data
      }
    })
    handleApiError(error, 'updateUserInfo')
  }
} 