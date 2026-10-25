<template>
  <view class="page">
    <!-- 搜索 -->
    <view class="search-box-wrap">
      <input
        class="search-input"
        v-model="keyword"
        placeholder="搜索商品"
        confirm-type="search"
        @confirm="search"
      />
      <view class="search-btn" @click="search">搜索</view>
    </view>

    <view class="body">
      <!-- 左侧分类 -->
      <scroll-view class="side" scroll-y>
        <view
          :class="['side-item', activeCat === 0 ? 'active' : '']"
          @click="selectCat(0)"
        >全部</view>
        <view
          :class="['side-item', activeCat === c.id ? 'active' : '']"
          v-for="c in cats"
          :key="c.id"
          @click="selectCat(c.id)"
        >{{ c.name }}</view>
      </scroll-view>

      <!-- 右侧商品 -->
      <scroll-view class="main" scroll-y @scrolltolower="loadMore">
        <view class="goods-card" v-for="p in list" :key="p.id" @click="goDetail(p.id)">
          <image class="goods-img" :src="p.cover" mode="aspectFill" />
          <view class="goods-info">
            <view class="goods-name">{{ p.name }}</view>
            <view class="goods-sub">{{ p.subtitle }}</view>
            <view class="goods-price-row">
              <text class="goods-price">¥{{ p.price }}</text>
              <text class="goods-sales">已售{{ p.sales }}</text>
            </view>
          </view>
        </view>
        <view class="empty" v-if="!loading && !list.length">暂无商品</view>
        <view class="load-more" v-if="list.length">{{ finished ? '— 没有更多了 —' : '加载中...' }}</view>
      </scroll-view>
    </view>
  </view>
</template>

<script>
import { api } from '../../api/index.js'

export default {
  data() {
    return {
      cats: [],
      activeCat: 0,
      keyword: '',
      list: [],
      page: 1,
      pageSize: 10,
      finished: false,
      loading: false
    }
  },
  onShow() {
    this.loadCategories()
    this.reload()
  },
  methods: {
    async loadCategories() {
      try {
        this.cats = await api.categories()
      } catch (e) {}
    },
    async reload() {
      this.page = 1
      this.finished = false
      this.list = []
      await this.loadProducts()
    },
    async loadProducts() {
      if (this.loading || this.finished) return
      this.loading = true
      try {
        const params = { page: this.page, page_size: this.pageSize }
        if (this.activeCat) params.category = this.activeCat
        if (this.keyword) params.keyword = this.keyword
        const data = await api.products(params)
        this.list = this.page === 1 ? data.results : this.list.concat(data.results)
        this.finished = this.list.length >= data.count
        this.page += 1
      } catch (e) {
      } finally {
        this.loading = false
      }
    },
    loadMore() {
      if (!this.finished) this.loadProducts()
    },
    selectCat(id) {
      this.activeCat = id
      this.reload()
    },
    search() {
      this.reload()
    },
    goDetail(id) {
      uni.navigateTo({ url: '/pages/product/detail?id=' + id })
    }
  }
}
</script>

<style lang="scss" scoped>
.page {
  display: flex;
  flex-direction: column;
  height: 100vh;
}
.search-box-wrap {
  display: flex;
  align-items: center;
  padding: 16rpx 24rpx;
  background: #fff;
}
.search-input {
  flex: 1;
  height: 64rpx;
  background: #f5f5f5;
  border-radius: 32rpx;
  padding: 0 28rpx;
  font-size: 26rpx;
}
.search-btn {
  margin-left: 20rpx;
  color: #e93b3d;
  font-size: 28rpx;
}
.body {
  flex: 1;
  display: flex;
  overflow: hidden;
}
.side {
  width: 176rpx;
  height: 100%;
  background: #f7f7f7;
}
.side-item {
  padding: 32rpx 0;
  text-align: center;
  font-size: 27rpx;
  color: #555;
}
.side-item.active {
  background: #fff;
  color: #e93b3d;
  font-weight: bold;
  border-left: 6rpx solid #e93b3d;
}
.main {
  flex: 1;
  height: 100%;
  padding: 16rpx;
  box-sizing: border-box;
}
.goods-card {
  display: flex;
  background: #fff;
  border-radius: 16rpx;
  margin-bottom: 16rpx;
  overflow: hidden;
  border: 1rpx solid #f0f0f0;
}
.goods-img {
  width: 180rpx;
  height: 180rpx;
  flex-shrink: 0;
}
.goods-info {
  flex: 1;
  padding: 16rpx;
  display: flex;
  flex-direction: column;
}
.goods-name {
  font-size: 27rpx;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.goods-sub {
  font-size: 22rpx;
  color: #999;
  margin-top: 8rpx;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.goods-price-row {
  display: flex;
  align-items: baseline;
  margin-top: auto;
}
.goods-price {
  color: #e93b3d;
  font-weight: bold;
  font-size: 32rpx;
}
.goods-sales {
  margin-left: auto;
  color: #bbb;
  font-size: 22rpx;
}
.load-more {
  text-align: center;
  color: #bbb;
  font-size: 24rpx;
  padding: 24rpx 0;
}
</style>
