// 小小新闻简报 - 首页逻辑
// pages/index/index.js

Page({
  data: {
    categories: ['时政', '科技', '体育', '教育', '军事', '娱乐', '健康', '环保'],
    selectedCategory: '时政',
    newsList: [],
    loading: false,
    page: 1,
    pageSize: 10
  },

  onLoad() {
    this.loadNews()
  },

  // 加载新闻
  loadNews() {
    this.setData({ loading: true })
    
    // 模拟API调用
    const mockNews = [
      {
        id: 1,
        title: '中国"人造太阳"装置实现千秒稳态运行',
        category: '时政',
        source: '央视新闻',
        snippet: '我国在上海临港成功实现1337秒稳态长脉冲运行，刷新商业核聚变世界纪录',
        image_url: 'https://via.placeholder.com/400x200?text=Sun',
        timestamp: '2026-03-26 06:14',
        views: 1234,
        likes: 567
      },
      {
        id: 2,
        title: '中国成功发射四维高景二号05、06星',
        category: '科技',
        source: '新华社',
        snippet: '长征二号丁运载火箭在太原卫星发射中心成功发射，卫星顺利进入预定轨道',
        image_url: 'https://via.placeholder.com/400x200?text=Rocket',
        timestamp: '2026-03-26 07:50',
        views: 890,
        likes: 345
      },
      {
        id: 3,
        title: '足坛一夜动态：姆巴佩澄清误诊传闻',
        category: '体育',
        source: '企鹅号',
        snippet: '足球明星姆巴佩澄清了误诊传闻，还维护了皇马队的医生',
        image_url: 'https://via.placeholder.com/400x200?text=Football',
        timestamp: '2026-03-26 06:42',
        views: 2100,
        likes: 890
      }
    ]
    
    this.setData({
      newsList: mockNews,
      loading: false
    })
  },

  // 选择分类
  selectCategory(e) {
    const category = e.currentTarget.dataset.category
    this.setData({
      selectedCategory: category,
      page: 1
    })
    this.loadNews()
  },

  // 查看新闻详情
  viewNews(e) {
    const newsId = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/detail/detail?id=${newsId}`
    })
  },

  // 点赞
  likeNews(e) {
    wx.showToast({
      title: '已点赞',
      icon: 'success',
      duration: 1000
    })
  },

  // 分享
  shareNews(e) {
    wx.showShareMenu({
      withShareTicket: true
    })
  },

  // 收藏
  collectNews(e) {
    wx.showToast({
      title: '已收藏',
      icon: 'success',
      duration: 1000
    })
  },

  // 加载更多
  loadMore() {
    this.setData({
      page: this.data.page + 1
    })
    this.loadNews()
  }
})
