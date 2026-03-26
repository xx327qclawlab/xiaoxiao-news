// 小小新闻简报 - 微信小程序
// app.js - 主程序文件

App({
  onLaunch() {
    // 初始化
    this.globalData = {
      userInfo: null,
      categories: ['时政', '科技', '体育', '教育', '军事', '娱乐', '健康', '环保'],
      selectedCategories: ['时政', '科技', '体育', '教育'],
      apiUrl: 'https://api.xiaoxiao-news.com'
    }
  },

  globalData: {
    userInfo: null
  }
})
