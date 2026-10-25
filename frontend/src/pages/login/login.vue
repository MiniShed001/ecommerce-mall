<template>
  <view class="page">
    <!-- 模式切换 -->
    <view class="mode-tabs">
      <view :class="['mode-tab', mode === 'login' ? 'on' : '']" @click="mode = 'login'">登录</view>
      <view :class="['mode-tab', mode === 'register' ? 'on' : '']" @click="mode = 'register'">注册</view>
    </view>

    <view class="form-card">
      <input class="form-input" v-model="username" placeholder="用户名" />
      <input class="form-input" v-model="password" :password="!showPwd" placeholder="密码（至少6位）" />
      <input v-if="mode === 'register'" class="form-input" v-model="phone" type="number" maxlength="11" placeholder="手机号（选填）" />
      <view class="show-pwd" @click="showPwd = !showPwd">{{ showPwd ? '隐藏密码' : '显示密码' }}</view>

      <view class="submit-btn" @click="submit">{{ mode === 'login' ? '登 录' : '注 册' }}</view>

      <view class="tip">
        <text>演示账号：demo / demo123456</text>
      </view>
    </view>
  </view>
</template>

<script>
import { api } from '../../api/index.js'

export default {
  data() {
    return {
      mode: 'login',
      username: '',
      password: '',
      phone: '',
      showPwd: false,
      submitting: false
    }
  },
  methods: {
    async submit() {
      if (!this.username || !this.password) {
        uni.showToast({ title: '请填写用户名和密码', icon: 'none' })
        return
      }
      if (this.submitting) return
      this.submitting = true
      try {
        if (this.mode === 'login') {
          const data = await api.login({ username: this.username, password: this.password })
          uni.setStorageSync('mall_token', data.access)
          uni.setStorageSync('mall_user', data.user)
          uni.showToast({ title: '登录成功', icon: 'success' })
          setTimeout(() => uni.navigateBack(), 800)
        } else {
          await api.register({
            username: this.username,
            password: this.password,
            phone: this.phone
          })
          uni.showToast({ title: '注册成功，请登录', icon: 'success' })
          this.mode = 'login'
          this.password = ''
        }
      } catch (e) {
        // 错误提示已由请求层统一处理
      } finally {
        this.submitting = false
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.page {
  padding: 60rpx 40rpx;
}
.mode-tabs {
  display: flex;
  justify-content: center;
  margin-bottom: 60rpx;
}
.mode-tab {
  font-size: 34rpx;
  color: #999;
  padding: 0 40rpx 16rpx;
  border-bottom: 4rpx solid transparent;
}
.mode-tab.on {
  color: #e93b3d;
  font-weight: bold;
  border-bottom-color: #e93b3d;
}
.form-card {
  background: #fff;
  border-radius: 20rpx;
  padding: 40rpx;
}
.form-input {
  height: 90rpx;
  border-bottom: 1rpx solid #f0f0f0;
  font-size: 30rpx;
}
.show-pwd {
  text-align: right;
  color: #999;
  font-size: 24rpx;
  padding: 20rpx 0 40rpx;
}
.submit-btn {
  background: #e93b3d;
  color: #fff;
  text-align: center;
  height: 88rpx;
  line-height: 88rpx;
  border-radius: 44rpx;
  font-size: 32rpx;
}
.tip {
  text-align: center;
  color: #bbb;
  font-size: 24rpx;
  margin-top: 30rpx;
}
</style>
