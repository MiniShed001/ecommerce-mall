import { del, get, patch, post } from './request'

export const api = {
  // ---------- 认证 ----------
  login: (data) => post('/api/auth/login/', data),
  register: (data) => post('/api/auth/register/', data),
  userInfo: () => get('/api/auth/user/'),
  updateUser: (data) => patch('/api/auth/user/', data),

  // ---------- 首页 / 商品 ----------
  home: () => get('/api/home/'),
  categories: () => get('/api/categories/'),
  products: (params) => get('/api/products/', params),
  productDetail: (id) => get(`/api/products/${id}/`),

  // ---------- 购物车 ----------
  cart: () => get('/api/cart/'),
  addCart: (data) => post('/api/cart/', data),
  updateCart: (id, data) => patch(`/api/cart/${id}/`, data),
  removeCart: (id) => del(`/api/cart/${id}/`),
  selectAllCart: (data) => post('/api/cart/select_all/', data),

  // ---------- 订单 ----------
  orders: (params) => get('/api/orders/list/', params),
  orderDetail: (id) => get(`/api/orders/${id}/`),
  createOrder: (data) => post('/api/orders/', data),
  payOrder: (id) => post(`/api/orders/${id}/pay/`),
  cancelOrder: (id) => post(`/api/orders/${id}/cancel/`)
}
