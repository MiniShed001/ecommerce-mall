<template>
  <view class="page">
    <view class="empty" v-if="!data.items.length && !loading">购物车空空如也～</view>

    <view class="cart-item" v-for="i in data.items" :key="i.id">
      <view :class="['checkbox', i.selected ? 'on' : '']" @click="toggle(i)"></view>
      <image class="item-img" :src="i.cover" mode="aspectFill" @click="goDetail(i.product_id)" />
      <view class="item-info">
        <view class="item-name" @click="goDetail(i.product_id)">{{ i.title }}</view>
        <view class="item-sub" v-if="i.stock < 10">仅剩 {{ i.stock }} 件</view>
        <view class="item-op">
          <view class="stepper">
            <view class="step-btn" @click="changeQty(i, -1)">-</view>
            <view class="step-num">{{ i.quantity }}</view>
            <view class="step-btn" @click="changeQty(i, 1)">+</view>
          </view>
          <view class="item-right">
            <text class="item-price">¥{{ i.subtotal }}</text>
            <view class="del-btn" @click="removeItem(i)">删除</view>
          </view>
        </view>
      </view>
    </view>

    <!-- 底部结算栏 -->
    <view class="bottom-bar" v-if="data.items.length">
      <view class="all-check" @click="toggleAll">
        <view :class="['checkbox', allSelected ? 'on' : '']"></view>
        <text>全选</text>
      </view>
      <view class="total">
        <text class="total-label">合计：</text>
        <text class="price">¥{{ data.total }}</text>
      </view>
      <view :class="['checkout', data.selected_count ? 'on' : '']" @click="checkout">
        结算({{ data.selected_count }})
      </view>
    </view>
  </view>
</template>

<script>
import { api } from '../../api/index.js'

export default {
  data() {
    return {
      loading: false,
      data: { items: [], count: 0, selected_count: 0, total: 0 }
    }
  },
  computed: {
    allSelected() {
      return this.data.items.length > 0 && this.data.items.every((i) => i.selected)
    }
  },
  onShow() {
    this.loadCart()
  },
  methods: {
    async loadCart() {
      this.loading = true
      try {
        this.data = await api.cart()
      } catch (e) {
      } finally {
        this.loading = false
      }
    },
    async toggle(item) {
      try {
        await api.updateCart(item.id, { selected: !item.selected })
        this.loadCart()
      } catch (e) {}
    },
    async toggleAll() {
      try {
        await api.selectAllCart({ selected: !this.allSelected })
        this.loadCart()
      } catch (e) {}
    },
    async changeQty(item, delta) {
      const quantity = item.quantity + delta
      if (quantity < 1) return
      try {
        await api.updateCart(item.id, { quantity })
        this.loadCart()
      } catch (e) {}
    },
    async removeItem(item) {
      const res = await uni.showModal({
        title: '提示',
        content: '确定删除该商品吗？'
      })
      if (!res.confirm) return
      try {
        await api.removeCart(item.id)
        this.loadCart()
      } catch (e) {}
    },
    checkout() {
      if (!this.data.selected_count) {
        uni.showToast({ title: '请先勾选商品', icon: 'none' })
        return
      }
      uni.navigateTo({ url: '/pages/order/confirm' })
    },
    goDetail(id) {
      uni.navigateTo({ url: '/pages/product/detail?id=' + id })
    }
  }
}
</script>

<style lang="scss" scoped>
.page {
  padding-bottom: 140rpx;
}
.cart-item {
  display: flex;
  align-items: center;
  background: #fff;
  margin: 16rpx 24rpx 0;
  border-radius: 16rpx;
  padding: 20rpx;
}
.checkbox {
  width: 40rpx;
  height: 40rpx;
  border-radius: 50%;
  border: 2rpx solid #ccc;
  margin-right: 20rpx;
  box-sizing: border-box;
  flex-shrink: 0;
}
.checkbox.on {
  background: #e93b3d;
  border-color: #e93b3d;
  position: relative;
}
.checkbox.on::after {
  content: '';
  position: absolute;
  left: 12rpx;
  top: 6rpx;
  width: 12rpx;
  height: 20rpx;
  border: solid #fff;
  border-width: 0 3rpx 3rpx 0;
  transform: rotate(45deg);
}
.item-img {
  width: 160rpx;
  height: 160rpx;
  border-radius: 12rpx;
  flex-shrink: 0;
}
.item-info {
  flex: 1;
  margin-left: 20rpx;
  min-width: 0;
}
.item-name {
  font-size: 28rpx;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.item-sub {
  font-size: 22rpx;
  color: #e93b3d;
  margin-top: 6rpx;
}
.item-op {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 16rpx;
}
.stepper {
  display: flex;
  align-items: center;
  border: 1rpx solid #e0e0e0;
  border-radius: 8rpx;
  overflow: hidden;
}
.step-btn {
  width: 56rpx;
  height: 52rpx;
  line-height: 52rpx;
  text-align: center;
  background: #f7f7f7;
  color: #333;
  font-size: 30rpx;
}
.step-num {
  width: 72rpx;
  height: 52rpx;
  line-height: 52rpx;
  text-align: center;
  font-size: 26rpx;
  border-left: 1rpx solid #e0e0e0;
  border-right: 1rpx solid #e0e0e0;
}
.item-right {
  display: flex;
  align-items: center;
}
.item-price {
  color: #e93b3d;
  font-weight: bold;
  font-size: 30rpx;
  margin-right: 20rpx;
}
.del-btn {
  color: #999;
  font-size: 24rpx;
}
.bottom-bar {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  background: #fff;
  display: flex;
  align-items: center;
  padding: 16rpx 24rpx;
  padding-bottom: calc(16rpx + env(safe-area-inset-bottom));
  box-shadow: 0 -2rpx 12rpx rgba(0, 0, 0, 0.05);
}
.all-check {
  display: flex;
  align-items: center;
  font-size: 26rpx;
  color: #555;
}
.total {
  margin-left: auto;
  margin-right: 24rpx;
}
.total-label {
  font-size: 26rpx;
  color: #555;
}
.checkout {
  background: #ffb4b5;
  color: #fff;
  border-radius: 40rpx;
  padding: 0 44rpx;
  height: 76rpx;
  line-height: 76rpx;
  font-size: 28rpx;
}
.checkout.on {
  background: #e93b3d;
}
</style>
