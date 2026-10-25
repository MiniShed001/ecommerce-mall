<template>
  <view class="page">
    <!-- 状态筛选 -->
    <view class="tabs">
      <view
        :class="['tab', active === 0 ? 'on' : '']"
        v-for="t in tabs"
        :key="t.value"
        @click="switchTab(t.value)"
      >{{ t.label }}</view>
    </view>

    <view class="empty" v-if="!loading && !list.length">暂无订单</view>

    <view class="order-card" v-for="o in list" :key="o.id">
      <view class="order-head">
        <text class="order-no">订单号：{{ o.order_no }}</text>
        <text class="order-status">{{ o.status_name }}</text>
      </view>
      <view class="order-item" v-for="(it, idx) in o.items" :key="idx" @click="goDetail(it.product_id)">
        <image class="item-img" :src="it.cover" mode="aspectFill" />
        <view class="item-info">
          <view class="item-name">{{ it.title }}</view>
          <view class="item-line">¥{{ it.price }} × {{ it.quantity }}</view>
        </view>
      </view>
      <view class="order-foot">
        <text class="order-time">{{ o.created_at }}</text>
        <text class="order-amount">实付：<text class="price">¥{{ o.total_amount }}</text></text>
      </view>
      <view class="order-actions">
        <view v-if="o.status === 0" class="act-btn plain" @click="cancel(o)">取消订单</view>
        <view v-if="o.status === 0" class="act-btn solid" @click="pay(o)">去支付</view>
        <view v-if="o.status === 1" class="act-btn plain">等待发货</view>
        <view v-if="o.status === 3" class="act-btn plain">交易完成</view>
      </view>
    </view>

    <view class="load-more" v-if="list.length">— 到底啦 —</view>
  </view>
</template>

<script>
import { api } from '../../api/index.js'

export default {
  data() {
    return {
      tabs: [
        { label: '全部', value: -1 },
        { label: '待支付', value: 0 },
        { label: '已支付', value: 1 },
        { label: '已完成', value: 3 },
        { label: '已取消', value: 4 }
      ],
      active: -1,
      list: [],
      loading: false
    }
  },
  onShow() {
    this.load()
  },
  methods: {
    async load() {
      this.loading = true
      try {
        const params = this.active === -1 ? {} : { status: this.active }
        this.list = await api.orders(params)
      } catch (e) {
      } finally {
        this.loading = false
      }
    },
    switchTab(v) {
      if (this.active === v) return
      this.active = v
      this.load()
    },
    async pay(order) {
      const res = await uni.showModal({ title: '提示', content: `确认支付 ¥${order.total_amount} 吗？（模拟支付）` })
      if (!res.confirm) return
      try {
        await api.payOrder(order.id)
        uni.showToast({ title: '支付成功', icon: 'success' })
        this.load()
      } catch (e) {}
    },
    async cancel(order) {
      const res = await uni.showModal({ title: '提示', content: '确定取消该订单吗？' })
      if (!res.confirm) return
      try {
        await api.cancelOrder(order.id)
        uni.showToast({ title: '已取消', icon: 'none' })
        this.load()
      } catch (e) {}
    },
    goDetail(id) {
      if (id) uni.navigateTo({ url: '/pages/product/detail?id=' + id })
    }
  }
}
</script>

<style lang="scss" scoped>
.tabs {
  display: flex;
  background: #fff;
  position: sticky;
  top: 0;
  z-index: 10;
}
.tab {
  flex: 1;
  text-align: center;
  padding: 24rpx 0;
  font-size: 28rpx;
  color: #555;
}
.tab.on {
  color: #e93b3d;
  font-weight: bold;
  border-bottom: 4rpx solid #e93b3d;
}
.order-card {
  background: #fff;
  margin: 20rpx 24rpx 0;
  border-radius: 16rpx;
  padding: 24rpx;
}
.order-head {
  display: flex;
  justify-content: space-between;
  padding-bottom: 16rpx;
  border-bottom: 1rpx solid #f0f0f0;
}
.order-no {
  font-size: 24rpx;
  color: #999;
}
.order-status {
  font-size: 26rpx;
  color: #e93b3d;
}
.order-item {
  display: flex;
  padding: 20rpx 0;
}
.item-img {
  width: 130rpx;
  height: 130rpx;
  border-radius: 12rpx;
  flex-shrink: 0;
}
.item-info {
  flex: 1;
  margin-left: 20rpx;
  min-width: 0;
}
.item-name {
  font-size: 27rpx;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.item-line {
  font-size: 24rpx;
  color: #999;
  margin-top: 10rpx;
}
.order-foot {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12rpx 0;
  border-top: 1rpx solid #f0f0f0;
}
.order-time {
  font-size: 24rpx;
  color: #999;
}
.order-amount {
  font-size: 26rpx;
}
.order-actions {
  display: flex;
  justify-content: flex-end;
}
.act-btn {
  margin-left: 20rpx;
  padding: 0 32rpx;
  height: 60rpx;
  line-height: 60rpx;
  border-radius: 30rpx;
  font-size: 26rpx;
}
.act-btn.plain {
  border: 1rpx solid #ddd;
  color: #555;
}
.act-btn.solid {
  background: #e93b3d;
  color: #fff;
}
.load-more {
  text-align: center;
  color: #bbb;
  font-size: 24rpx;
  padding: 40rpx 0;
}
</style>
