<template>
  <view class="page" v-if="p.id">
    <!-- 轮播图 -->
    <swiper class="gallery" circular indicator-dots v-if="p.gallery && p.gallery.length">
      <swiper-item v-for="(g, i) in p.gallery" :key="i">
        <image class="gallery-img" :src="g" mode="aspectFill" />
      </swiper-item>
    </swiper>
    <image v-else class="gallery-img" :src="p.cover" mode="aspectFill" />

    <!-- 价格区 -->
    <view class="price-bar">
      <view class="prices">
        <text class="price">¥{{ p.price }}</text>
        <text class="origin" v-if="p.original_price > 0">¥{{ p.original_price }}</text>
      </view>
      <view class="meta">库存 {{ p.stock }} · 已售 {{ p.sales }}</view>
    </view>

    <!-- 标题 -->
    <view class="info-card">
      <view class="name">{{ p.name }}</view>
      <view class="sub">{{ p.subtitle }}</view>
    </view>

    <!-- 详情 -->
    <view class="detail-card">
      <view class="detail-title">商品详情</view>
      <text class="detail-text" selectable>{{ p.detail }}</text>
    </view>

    <!-- 底部操作 -->
    <view class="bottom-bar">
      <view class="bar-btn" @click="goCart">购物车</view>
      <view class="bar-btn warn" @click="addCart">加入购物车</view>
      <view class="bar-btn danger" @click="buyNow">立即购买</view>
    </view>
  </view>
</template>

<script>
import { api } from '../../api/index.js'

export default {
  data() {
    return {
      id: 0,
      p: {},
      quantity: 1
    }
  },
  onLoad(options) {
    this.id = Number(options.id)
    this.loadDetail()
  },
  methods: {
    async loadDetail() {
      try {
        this.p = await api.productDetail(this.id)
      } catch (e) {}
    },
    needLogin() {
      const token = uni.getStorageSync('mall_token')
      if (!token) {
        uni.showToast({ title: '请先登录', icon: 'none' })
        setTimeout(() => uni.navigateTo({ url: '/pages/login/login' }), 600)
        return true
      }
      return false
    },
    async addCart() {
      if (this.needLogin()) return
      try {
        await api.addCart({ product_id: this.id, quantity: this.quantity })
        uni.showToast({ title: '已加入购物车', icon: 'success' })
      } catch (e) {}
    },
    buyNow() {
      if (this.needLogin()) return
      // 立即购买：把商品快照交给确认订单页
      uni.setStorageSync('mall_buy_now', {
        product_id: this.p.id,
        title: this.p.name,
        cover: this.p.cover,
        price: this.p.price,
        quantity: this.quantity
      })
      uni.navigateTo({ url: '/pages/order/confirm' })
    },
    goCart() {
      uni.switchTab({ url: '/pages/cart/cart' })
    }
  }
}
</script>

<style lang="scss" scoped>
.page {
  padding-bottom: 120rpx;
}
.gallery {
  width: 100%;
  height: 750rpx;
}
.gallery-img {
  width: 100%;
  height: 750rpx;
}
.price-bar {
  background: #fff;
  padding: 24rpx;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
}
.prices {
  display: flex;
  align-items: baseline;
}
.price {
  font-size: 44rpx;
}
.origin {
  color: #bbb;
  text-decoration: line-through;
  font-size: 24rpx;
  margin-left: 16rpx;
}
.meta {
  color: #999;
  font-size: 24rpx;
}
.info-card {
  background: #fff;
  margin-top: 16rpx;
  padding: 24rpx;
}
.name {
  font-size: 34rpx;
  font-weight: bold;
  color: #333;
}
.sub {
  font-size: 26rpx;
  color: #999;
  margin-top: 12rpx;
}
.detail-card {
  background: #fff;
  margin-top: 16rpx;
  padding: 24rpx;
}
.detail-title {
  font-size: 30rpx;
  font-weight: bold;
  margin-bottom: 16rpx;
}
.detail-text {
  font-size: 26rpx;
  color: #555;
  line-height: 1.8;
  white-space: pre-line;
}
.bottom-bar {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  background: #fff;
  display: flex;
  padding: 16rpx 24rpx;
  padding-bottom: calc(16rpx + env(safe-area-inset-bottom));
  box-shadow: 0 -2rpx 12rpx rgba(0, 0, 0, 0.05);
}
.bar-btn {
  flex: 1;
  text-align: center;
  line-height: 76rpx;
  border-radius: 40rpx;
  border: 1rpx solid #ddd;
  color: #333;
  font-size: 28rpx;
  margin-right: 16rpx;
}
.bar-btn.warn {
  background: #ff9500;
  color: #fff;
  border: none;
}
.bar-btn.danger {
  background: #e93b3d;
  color: #fff;
  border: none;
  margin-right: 0;
}
</style>
