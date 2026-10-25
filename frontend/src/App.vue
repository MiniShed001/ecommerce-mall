<script>
export default {
  onLaunch() {
    // 启动时自动恢复登录态（token 在本地存储）
    console.log('全栈电商启动，登录态:', !!uni.getStorageSync('mall_token'))
  }
}
</script>

<style>
/* 全局样式 */
page {
  background: #f5f5f5;
  font-size: 28rpx;
  color: #333;
}

.price {
  color: #e93b3d;
  font-weight: bold;
}

.btn-primary {
  background: #e93b3d;
  color: #fff;
  border-radius: 40rpx;
}

.empty {
  text-align: center;
  color: #999;
  padding: 200rpx 0;
  font-size: 30rpx;
}
</style>
