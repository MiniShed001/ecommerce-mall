<template>
  <view class="page">
    <!-- 用户信息头 -->
    <view class="header">
      <view class="avatar" @click="goLogin">
        <image v-if="user && user.avatar" class="avatar-img" :src="user.avatar" mode="aspectFill" />
        <text v-else class="avatar-text">{{ (user && user.nickname) ? user.nickname[0] : '登' }}</text>
      </view>
      <view class="user-info" @click="goLogin">
        <view class="nickname">{{ user ? (user.nickname || user.username) : '点击登录' }}</view>
        <view class="phone">{{ user ? (user.phone || user.username) : '登录后同步购物车与订单' }}</view>
      </view>
      <view class="logout" v-if="isLogin" @click="logout">退出</view>
    </view>

    <!-- 订单入口 -->
    <view class="card" @click="goOrders">
      <view class="card-row">
        <text class="card-label">我的订单</text>
        <text class="card-arrow">全部订单 ›</text>
      </view>
      <view class="order-grid">
        <view class="order-item" @click.stop="goOrders(0)">
          <view class="order-icon">待</view>
          <text class="order-text">待支付</text>
        </view>
        <view class="order-item" @click.stop="goOrders(1)">
          <view class="order-icon">已</view>
          <text class="order-text">已支付</text>
        </view>
        <view class="order-item" @click.stop="goOrders(3)">
          <view class="order-icon">完</view>
          <text class="order-text">已完成</text>
        </view>
        <view class="order-item" @click.stop="goOrders(4)">
          <view class="order-icon">退</view>
          <text class="order-text">已取消</text>
        </view>
      </view>
    </view>

    <!-- 功能菜单 -->
    <view class="card">
      <view class="menu-row" @click="tip('收货地址')">
        <text class="menu-label">收货地址</text>
        <text class="card-arrow">›</text>
      </view>
      <view class="menu-row" @click="tip('联系客服')">
        <text class="menu-label">联系客服</text>
        <text class="card-arrow">›</text>
      </view>
      <view class="menu-row" @click="tip('关于我们')">
        <text class="menu-label">关于我们</text>
        <text class="card-arrow">›</text>
      </view>
    </view>

    <view class="version">全栈电商 v1.0 · UniApp → Nginx → Django → Redis</view>
  </view>
</template>

<script>
import { api } from '../../api/index.js'

export default {
  data() {
    return {
      user: null,
      isLogin: false
    }
  },
  onShow() {
    this.isLogin = !!uni.getStorageSync('mall_token')
    this.user = uni.getStorageSync('mall_user') || null
    if (this.isLogin && !this.user) this.fetchUser()
  },
  methods: {
    async fetchUser() {
      try {
        this.user = await api.userInfo()
        uni.setStorageSync('mall_user', this.user)
      } catch (e) {}
    },
    goLogin() {
      if (!this.isLogin) uni.navigateTo({ url: '/pages/login/login' })
    },
    goOrders(status) {
      if (!this.isLogin) {
        uni.navigateTo({ url: '/pages/login/login' })
        return
      }
      const url = status === undefined
        ? '/pages/order/list'
        : `/pages/order/list?status=${status}`
      uni.navigateTo({ url })
    },
    logout() {
      uni.removeStorageSync('mall_token')
      uni.removeStorageSync('mall_user')
      this.isLogin = false
      this.user = null
      uni.showToast({ title: '已退出登录', icon: 'none' })
    },
    tip(name) {
      uni.showToast({ title: name + '：演示功能', icon: 'none' })
    }
  }
}
</script>

<style lang="scss" scoped>
.header {
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #e93b3d, #ff6b6b);
  padding: 60rpx 40rpx;
}
.avatar {
  width: 120rpx;
  height: 120rpx;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.25);
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}
.avatar-img {
  width: 100%;
  height: 100%;
}
.avatar-text {
  color: #fff;
  font-size: 44rpx;
}
.user-info {
  flex: 1;
  margin-left: 24rpx;
}
.nickname {
  color: #fff;
  font-size: 36rpx;
  font-weight: bold;
}
.phone {
  color: rgba(255, 255, 255, 0.8);
  font-size: 24rpx;
  margin-top: 10rpx;
}
.logout {
  color: rgba(255, 255, 255, 0.9);
  font-size: 26rpx;
  border: 1rpx solid rgba(255, 255, 255, 0.6);
  border-radius: 30rpx;
  padding: 8rpx 24rpx;
}
.card {
  background: #fff;
  margin: 20rpx 24rpx 0;
  border-radius: 16rpx;
  padding: 24rpx;
}
.card-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.card-label {
  font-size: 30rpx;
  font-weight: bold;
}
.card-arrow {
  font-size: 26rpx;
  color: #999;
}
.order-grid {
  display: flex;
  padding-top: 24rpx;
}
.order-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.order-icon {
  width: 72rpx;
  height: 72rpx;
  border-radius: 20rpx;
  background: #fdecec;
  color: #e93b3d;
  font-size: 30rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}
.order-text {
  font-size: 24rpx;
  color: #555;
  margin-top: 12rpx;
}
.menu-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 28rpx 0;
  border-bottom: 1rpx solid #f7f7f7;
}
.menu-row:last-child {
  border-bottom: none;
}
.menu-label {
  font-size: 28rpx;
  color: #333;
}
.version {
  text-align: center;
  color: #bbb;
  font-size: 22rpx;
  padding: 60rpx 0 40rpx;
}
</style>
