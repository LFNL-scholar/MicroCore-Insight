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

/**
 * 更新设备昵称
 * @param {string|number} deviceId - 设备ID
 * @param {string} deviceName - 新的设备昵称
 * @param {string} userId - 用户ID
 * @returns {Promise<Object>} - 更新结果
 */
export async function updateDeviceName(deviceId, deviceName, userId) {
  try {
    const response = await api.put('/api/frontend/device/update', {
      user_id: userId,
      device_4id: deviceId,
      device_name: deviceName
    })
    
    console.log('Update device name response:', response.data)
    
    if (response.data.status === 'success') {
      return response.data
    }
    
    throw new Error(response.data.message || '更新设备昵称失败')
  } catch (error) {
    console.error('Update device name error:', {
      method: 'PUT',
      url: '/api/frontend/device/update',
      data: {
        user_id: userId,
        device_4id: deviceId,
        device_name: deviceName
      },
      error: {
        message: error.message,
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data
      }
    })

    if (error.response?.status === 400) {
      throw new Error('参数缺失，请检查输入')
    }
    
    if (error.response?.status === 500) {
      throw new Error('服务器内部错误，请稍后重试')
    }
    
    handleApiError(error, 'updateDeviceName')
  }
}

/**
 * 获取设备详细信息
 * @param {string|number} deviceId - 设备ID
 * @param {string} userId - 用户ID
 * @returns {Promise<Object>} - 设备详细信息
 */
export async function getDeviceDetail(deviceId, userId) {
  try {
    const response = await api.get('/api/frontend/device/info', {
      params: {
        user_id: userId,
        device_4id: deviceId.toString()
      }
    })
    
    console.log('Get device detail response:', response.data)
    
    if (response.data.status === 'success') {
      return response.data
    }
    
    throw new Error(response.data.message || '获取设备详情失败')
  } catch (error) {
    console.error('Get device detail error:', {
      method: 'GET',
      url: '/api/frontend/device/info',
      params: {
        user_id: userId,
        device_4id: deviceId
      },
      error: {
        message: error.message,
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data
      }
    })
    
    if (error.response?.status === 404) {
      throw new Error('设备不存在')
    }
    
    if (error.response?.status === 500) {
      throw new Error('服务器内部错误，请稍后重试')
    }
    
    handleApiError(error, 'getDeviceDetail')
  }
}

/**
 * 删除设备
 * @param {string} userId - 用户ID
 * @param {string} macAddress - 设备MAC地址
 * @returns {Promise<Object>} - 删除结果
 */
export async function deleteDevice(userId, macAddress) {
  try {
    const response = await api.delete('/api/frontend/user/delete', {
      data: {
        user_id: userId,
        mac_address: macAddress
      }
    })
    
    console.log('Delete device response:', response.data)
    
    if (response.data.status === 'success') {
      return response.data
    }
    
    throw new Error(response.data.message || '删除设备失败')
  } catch (error) {
    console.error('Delete device error:', {
      method: 'DELETE',
      url: '/api/frontend/user/delete',
      data: {
        user_id: userId,
        mac_address: macAddress
      },
      error: {
        message: error.message,
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data
      }
    })

    if (error.response?.status === 404) {
      throw new Error('设备不存在')
    }
    
    if (error.response?.status === 500) {
      throw new Error('服务器内部错误，请稍后重试')
    }
    
    handleApiError(error, 'deleteDevice')
  }
}
