<template>
  <view class="page">
    <!-- 搜索栏 -->
    <view class="search-bar" @click="goSearch">
      <view class="search-box">
        <text class="search-icon">&#128269;</text>
        <text class="search-placeholder">搜索商品</text>
      </view>
    </view>

    <!-- 轮播图（来自 Redis 缓存接口 /api/home/） -->
    <swiper v-if="home.banners.length" class="banner" indicator-dots circular autoplay interval="4000">
      <swiper-item v-for="b in home.banners" :key="b.id" @click="goDetail(b.id)">
        <image class="banner-img" :src="b.image" mode="aspectFill" />
      </swiper-item>
    </swiper>

    <!-- 分类入口 -->
    <view class="cat-grid" v-if="home.categories.length">
      <view
        class="cat-item"
        v-for="(c, idx) in home.categories"
        :key="c.id"
        @click="goCategory"
      >
        <view class="cat-block" :style="{ background: colors[idx % colors.length] }">{{ c.name[0] }}</view>
        <text class="cat-name">{{ c.name }}</text>
      </view>
    </view>

    <!-- 热门推荐 -->
    <view class="section" v-if="home.hot.length">
      <view class="section-title"><text class="title-line"></text>热门推荐</view>
      <view class="goods-grid">
        <view class="goods-card" v-for="p in home.hot" :key="p.id" @click="goDetail(p.id)">
          <image class="goods-img" :src="p.cover" mode="aspectFill" />
          <view class="goods-name">{{ p.name }}</view>
          <view class="goods-sub">{{ p.subtitle }}</view>
          <view class="goods-price-row">
            <text class="goods-price">¥{{ p.price }}</text>
            <text class="goods-sales">已售{{ p.sales }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 新品上架 -->
    <view class="section" v-if="home.new.length">
      <view class="section-title"><text class="title-line"></text>新品上架</view>
      <view class="goods-card-row" v-for="p in home.new" :key="p.id" @click="goDetail(p.id)">
        <image class="row-img" :src="p.cover" mode="aspectFill" />
        <view class="row-info">
          <view class="goods-name">{{ p.name }}</view>
          <view class="goods-sub">{{ p.subtitle }}</view>
          <view class="goods-price-row">
            <text class="goods-price">¥{{ p.price }}</text>
            <text class="goods-origin" v-if="p.original_price > 0">¥{{ p.original_price }}</text>
            <text class="goods-sales">已售{{ p.sales }}</text>
          </view>
        </view>
      </view>
    </view>

    <view class="footer-tip" v-if="!loading && !home.hot.length && !home.new.length">暂无数据，请检查后端服务</view>
  </view>
</template>

<script>
import { api } from '../../api/index.js'

export default {
  data() {
    return {
      loading: false,
      home: { banners: [], hot: [], new: [], categories: [] },
      colors: ['#e93b3d', '#ff9500', '#34c759', '#5856d6', '#ff2d55', '#00c7be']
    }
  },
  onLoad() {
    this.loadHome()
  },
  onPullDownRefresh() {
    this.loadHome().finally(() => uni.stopPullDownRefresh())
  },
  methods: {
    async loadHome() {
      this.loading = true
      try {
        this.home = await api.home()
      } catch (e) {
        // 错误提示已由请求层统一处理
      } finally {
        this.loading = false
      }
    },
    goDetail(id) {
      uni.navigateTo({ url: '/pages/product/detail?id=' + id })
    },
    goSearch() {
      uni.switchTab({ url: '/pages/category/category' })
    },
    goCategory() {
      uni.switchTab({ url: '/pages/category/category' })
    }
  }
}
</script>

<style lang="scss" scoped>
.page {
  padding-bottom: 40rpx;
}

/* 搜索栏 */
.search-bar {
  padding: 16rpx 24rpx;
  background: #e93b3d;
}
.search-box {
  display: flex;
  align-items: center;
  background: #fff;
  border-radius: 36rpx;
  height: 64rpx;
  padding: 0 24rpx;
}
.search-icon {
  font-size: 28rpx;
  margin-right: 12rpx;
}
.search-placeholder {
  color: #999;
  font-size: 26rpx;
}

/* 轮播 */
.banner {
  height: 320rpx;
  width: 100%;
}
.banner-img {
  width: 100%;
  height: 320rpx;
}

/* 分类 */
.cat-grid {
  display: flex;
  flex-wrap: wrap;
  background: #fff;
  padding: 24rpx 12rpx;
}
.cat-item {
  width: 25%;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 24rpx;
}
.cat-block {
  width: 88rpx;
  height: 88rpx;
  border-radius: 24rpx;
  color: #fff;
  font-size: 36rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}
.cat-name {
  font-size: 24rpx;
  color: #333;
  margin-top: 10rpx;
}

/* 分区 */
.section {
  margin-top: 20rpx;
  background: #fff;
  padding: 24rpx 24rpx 8rpx;
}
.section-title {
  font-size: 32rpx;
  font-weight: bold;
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
}
.title-line {
  width: 8rpx;
  height: 30rpx;
  background: #e93b3d;
  border-radius: 4rpx;
  margin-right: 14rpx;
}

/* 商品双列 */
.goods-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}
.goods-card {
  width: 48%;
  background: #fff;
  border-radius: 16rpx;
  margin-bottom: 20rpx;
  overflow: hidden;
  border: 1rpx solid #f0f0f0;
}
.goods-img {
  width: 100%;
  height: 340rpx;
}
.goods-name {
  font-size: 27rpx;
  color: #333;
  padding: 12rpx 16rpx 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.goods-sub {
  font-size: 22rpx;
  color: #999;
  padding: 6rpx 16rpx 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.goods-price-row {
  display: flex;
  align-items: baseline;
  padding: 10rpx 16rpx 18rpx;
}
.goods-price {
  color: #e93b3d;
  font-weight: bold;
  font-size: 32rpx;
}
.goods-origin {
  color: #bbb;
  text-decoration: line-through;
  font-size: 22rpx;
  margin-left: 10rpx;
}
.goods-sales {
  margin-left: auto;
  color: #bbb;
  font-size: 22rpx;
}

/* 新品单行卡片 */
.goods-card-row {
  display: flex;
  background: #fff;
  border-radius: 16rpx;
  border: 1rpx solid #f0f0f0;
  margin-bottom: 20rpx;
  overflow: hidden;
}
.row-img {
  width: 200rpx;
  height: 200rpx;
  flex-shrink: 0;
}
.row-info {
  flex: 1;
  padding: 18rpx;
  display: flex;
  flex-direction: column;
}
.footer-tip {
  text-align: center;
  color: #999;
  padding: 80rpx 0;
}
</style>
