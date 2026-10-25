/**
 * 轻量全局状态（token / 用户信息）
 * 依赖 uni 本地存储持久化，无第三方状态库，兼容 H5 / App / 小程序
 */
const TOKEN_KEY = 'mall_token'
const USER_KEY = 'mall_user'

const store = {
  token: uni.getStorageSync(TOKEN_KEY) || '',
  user: uni.getStorageSync(USER_KEY) || null,

  get isLogin() {
    return !!this.token
  },

  setToken(token) {
    this.token = token || ''
    if (token) uni.setStorageSync(TOKEN_KEY, token)
    else uni.removeStorageSync(TOKEN_KEY)
  },

  setUser(user) {
    this.user = user || null
    if (user) uni.setStorageSync(USER_KEY, user)
    else uni.removeStorageSync(USER_KEY)
  },

  logout() {
    this.setToken('')
    this.setUser(null)
  }
}

export default store
