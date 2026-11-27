# A–H 平台适配器索引 V2.0

| Mode | 平台 | 主要入口 | 适配器 |
|---|---|---|---|
| A | 抖音短视频 | 推荐流、搜索、主页、视频封面/首帧 | platforms/A-douyin.md |
| B | 微信视频号 | 推荐、好友分享、主页 | platforms/B-wechat-channels.md |
| C | 小红书 | 发现、搜索、笔记/视频封面 | platforms/C-xiaohongshu.md |
| D | 闲鱼 | 搜索、商品/服务列表、首图 | platforms/D-xianyu.md |
| E | 淘宝/天猫 | 搜索、推荐、主图、SKU、详情 | platforms/E-taobao-tmall.md |
| F | 抖音商城 | 商城搜索、猜你喜欢、商品卡 | platforms/F-douyin-mall.md |
| G | 抖音电商直播 | 直播预告、直播间封面、场景 | platforms/G-douyin-live.md |
| H | 淘宝直播 | 直播入口、预告、直播间封面 | platforms/H-taobao-live.md |

先确定 platform_mode + surface；平台名不足以确定素材规格。每篇选一个主类型，最多一个辅助类型；注意力入口单独选择。A/B/C 继续 V5.1 12/18 字素簇默认预算；D–H 不继承。平台规格、类目准入和后台字段未知时标记 PLATFORM_SPEC_PENDING / UNKNOWN。不要把公开算法说明推导成封面权重、CTR 门槛或流量保证。
