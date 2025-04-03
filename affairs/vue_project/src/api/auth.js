import api, { handleApiError } from './request'

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

// 更新密码服务
export const updatePassword = async (userId, oldPassword, newPassword) => {
  try {
    const response = await api.post('/api/auth/update-password', {
      user_id: userId,
      old_password: oldPassword,
      new_password: newPassword
    })
    return response.data
  } catch (error) {
    handleApiError(error, 'updatePassword')
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