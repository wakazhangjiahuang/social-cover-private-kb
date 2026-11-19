# 平台与开源来源版本、许可和采用边界

核验日期：2026-11-01。来源快照不是永久结论；每次任务按需刷新。

## 平台官方/原始研究

完整来源 ID、URL、支持范围和限制见 `platform-source-registry.json`。优先级：官方平台/监管部门 > 平台团队公开论文 > 原始 GitHub 项目 > 第三方经验。

重点研究：
- 小红书 GenRank（Explore Feed 推荐排序）
- 小红书 KDD 2026 Search Relevance（搜索 query-note 相关性）
- 小红书 NoteLLM、IDProxy（笔记语义与多模态冷启动）
- 抖音安全与信任中心公开推荐系统说明
- 中央网信办对视频号“好友推荐+算法推荐”双机制的公开说明
- 国家 AI 生成合成内容标识办法

## 新增 GitHub 项目

| 项目 | commit | 许可 | 采用方法 | 不采用 |
|---|---|---|---|---|
| atian-create/xhs-cover-lab-open-skill | `2cb8ac794d42027b9fae20b131c7c424deff344b` | MIT | 小红书封面类型/赛道路由/Brief | 不复制完整 Prompt，不宣称 CTR |
| Jsanks-su/ASU-Douyin-Cover-Skill | `eccee49330f9af8799baa265c74bb6ba3ba92901` | 无 LICENSE | 抖音封面实图匹配、裁切、验收 | 不复制 170 张图库/源码 |
| zhengzhentao86/douyin-content-strategy-skill | `d296471fdbe7452225f186c7096b3a26ea233df5` | 无 LICENSE | 商品买点→人群→场景→内容策略链 | 不复制课程/提示词/示例 |
| ahang008/ah-douyin-cover-title | `86e38b5343e122bafe66ee86efb6e91bd156f4b3` | MIT | 标题钩子分类作为灵感 | 不把 85 条案例称为平台验证公式 |
| tuihou123321/wechat-channels-knowledge-cover | `f5d7167f258d82a794a0762f01bb32c84570bd3f` | 无 LICENSE | 视频号知识封面标题与人像裁切的样本观察 | 不复制代码/示例；7–15 字不是官方阈值 |
| JamesWuHK/wechat-video-channel-publish-skill | `67ebe674a5d633f9209b5de3059c4e37eb2afd64` | 无 LICENSE | 视频号发布器封面字段和页面流程观察 | 不复制发布自动化实现 |
| ToBeWin/covercraft-skill | `db4a898dc4cd87a52c897adbd0d42f0dfc75cc31` | 无 LICENSE | 跨平台工作流分层思路 | 不复制源码/模板 |
| ToBeWin/wechat-article-video-skill | `2cffe85faf256da5d3f570ba1f019200fa074947` | README 声明 MIT-0 | 视频号视频首帧与独立上传封面分离 | 不复制视频生产代码 |
| oil-oil/video-publisher-skill | `0d02cc5387b0bea0a43d5aa4e72a2c9502d05f94` | MIT | 多平台封面槽、页面适配和发布前验收 | 不把页面尺寸经验当算法规则 |

## 许可政策

- 没有 LICENSE 文件或许可无法核验：仅记录来源与独立总结的方法，不复制源码、模板、图片、字体或完整 Prompt。
- 有开源许可证：仍只提取完成本 Skill 所需的抽象方法；若未来复制代码或资产，重新核对当前版本与许可证义务。
- 第三方参考图、博主肖像、Logo、账号水印和原创角色不因公开仓库而自动获得再许可。
