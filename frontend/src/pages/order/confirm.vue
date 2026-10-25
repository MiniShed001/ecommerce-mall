<template>
  <view class="page">
    <!-- 收货信息 -->
    <view class="card addr-card">
      <view class="card-title">收货信息</view>
      <input class="addr-input" v-model="form.receiver_name" placeholder="收货人姓名" />
      <input class="addr-input" v-model="form.receiver_phone" type="number" placeholder="手机号" maxlength="11" />
      <input class="addr-input" v-model="form.receiver_address" placeholder="详细地址（省市区+街道门牌）" />
    </view>

    <!-- 商品清单 -->
    <view class="card">
      <view class="card-title">商品清单（{{ totalQty }} 件）</view>
      <view class="item" v-for="(i, idx) in items" :key="idx">
        <image class="item-img" :src="i.cover" mode="aspectFill" />
        <view class="item-info">
          <view class="item-name">{{ i.title }}</view>
          <view class="item-line">¥{{ i.price }} × {{ i.quantity }}</view>
        </view>
      </view>
      <view class="total-line">
        合计：<text class="price">¥{{ total }}</text>
      </view>
    </view>

    <!-- 备注 -->
    <view class="card">
      <input class="addr-input" v-model="form.remark" placeholder="订单备注（选填）" />
    </view>

    <!-- 提交 -->
    <view class="submit-bar">
      <view class="submit-total">
        应付：<text class="price">¥{{ total }}</text>
      </view>
      <view class="submit-btn" @click="submit">提交订单</view>
    </view>
  </view>
</template>

<script>
import { api } from '../../api/index.js'

export default {
  data() {
    return {
      buyNow: null, // 立即购买快照
      items: [],
      form: {
        receiver_name: '',
        receiver_phone: '',
        receiver_address: '',
        remark: ''
      },
      loading: false
    }
  },
  computed: {
    total() {
      return this.items
        .reduce((sum, i) => sum + Number(i.price) * i.quantity, 0)
        .toFixed(2)
    },
    totalQty() {
      return this.items.reduce((sum, i) => sum + i.quantity, 0)
    }
  },
  onLoad() {
    this.buyNow = uni.getStorageSync('mall_buy_now') || null
    this.loadItems()
  },
  onUnload() {
    // 离开页面清理立即购买快照
    uni.removeStorageSync('mall_buy_now')
  },
  methods: {
    async loadItems() {
      if (this.buyNow) {
        this.items = [this.buyNow]
        return
      }
      try {
        const data = await api.cart()
        this.items = data.items.filter((i) => i.selected)
      } catch (e) {}
    },
    validate() {
      if (!this.form.receiver_name) return '请填写收货人'
      if (!/^1\d{10}$/.test(this.form.receiver_phone)) return '请填写正确的手机号'
      if (!this.form.receiver_address) return '请填写收货地址'
      return ''
    },
    async submit() {
      const err = this.validate()
      if (err) {
        uni.showToast({ title: err, icon: 'none' })
        return
      }
      if (this.loading) return
      this.loading = true
      try {
        const payload = {
          receiver_name: this.form.receiver_name,
          receiver_phone: this.form.receiver_phone,
          receiver_address: this.form.receiver_address,
          remark: this.form.remark
        }
        if (this.buyNow) {
          payload.items = [{ product_id: this.buyNow.product_id, quantity: this.buyNow.quantity }]
          payload.from_cart = false
        }
        const order = await api.createOrder(payload)
        uni.showToast({ title: '下单成功', icon: 'success' })
        uni.removeStorageSync('mall_buy_now')
        setTimeout(() => {
          uni.redirectTo({ url: '/pages/order/list?highlight=' + order.id })
        }, 800)
      } catch (e) {
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.page {
  padding-bottom: 140rpx;
}
.card {
  background: #fff;
  margin: 20rpx 24rpx 0;
  border-radius: 16rpx;
  padding: 24rpx;
}
.card-title {
  font-size: 30rpx;
  font-weight: bold;
  margin-bottom: 16rpx;
}
.addr-input {
  height: 72rpx;
  border-bottom: 1rpx solid #f0f0f0;
  font-size: 27rpx;
}
.item {
  display: flex;
  margin-bottom: 20rpx;
}
.item-img {
  width: 140rpx;
  height: 140rpx;
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
.item-line {
  font-size: 26rpx;
  color: #999;
  margin-top: 12rpx;
}
.total-line {
  text-align: right;
  font-size: 28rpx;
  padding-top: 16rpx;
  border-top: 1rpx solid #f0f0f0;
}
.submit-bar {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 16rpx 24rpx;
  padding-bottom: calc(16rpx + env(safe-area-inset-bottom));
  box-shadow: 0 -2rpx 12rpx rgba(0, 0, 0, 0.05);
}
.submit-total {
  font-size: 28rpx;
  margin-right: 24rpx;
}
.submit-btn {
  background: #e93b3d;
  color: #fff;
  border-radius: 40rpx;
  padding: 0 56rpx;
  height: 76rpx;
  line-height: 76rpx;
  font-size: 28rpx;
}
</style>
