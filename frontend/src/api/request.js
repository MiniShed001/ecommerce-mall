/**
 * 统一请求封装
 * 链路：H5 页面 -> Nginx(8080) -> 同源 /api -> Django(8000) -> Redis -> DB
 * BASE_URL 留空走 Nginx 同源代理；HBuilderX 直连后端调试时改为 'http://localhost:8000'
 */
export const BASE_URL = ''
const TIMEOUT = 15000

export function request(options) {
  return new Promise((resolve, reject) => {
    const token = uni.getStorageSync('mall_token')
    uni.request({
      url: BASE_URL + options.url,
      method: options.method || 'GET',
      data: options.data || {},
      timeout: TIMEOUT,
      header: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: 'Bearer ' + token } : {}),
        ...(options.header || {})
      },
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data)
        } else if (res.statusCode === 401) {
          uni.removeStorageSync('mall_token')
          uni.removeStorageSync('mall_user')
          uni.showToast({ title: '登录已过期，请重新登录', icon: 'none' })
          setTimeout(() => {
            uni.navigateTo({ url: '/pages/login/login' })
          }, 800)
          reject(res.data)
        } else {
          const raw = res.data && res.data.detail
          const msg = typeof raw === 'string' ? raw : (raw && raw[0] && typeof raw[0] === 'string' ? raw[0] : '请求失败')
          uni.showToast({ title: msg, icon: 'none' })
          reject(res.data)
        }
      },
      fail: (err) => {
        uni.showToast({ title: '网络异常，请检查服务是否启动', icon: 'none' })
        reject(err)
      }
    })
  })
}

export const get = (url, data) => request({ url, method: 'GET', data })
export const post = (url, data) => request({ url, method: 'POST', data })
export const patch = (url, data) => request({ url, method: 'PATCH', data })
export const del = (url, data) => request({ url, method: 'DELETE', data })
