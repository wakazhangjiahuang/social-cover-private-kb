# social-cover-studio v1.9.6

按任务路由、三平台独立策略、真实资料、双层变量、参考图合同完成封面工作。

本版本重点校准标题决策：四层内部表达（目标客户利益→营销钩子→事件和关键词→证据补充），并明确四项审稿指标（用户视角、点击动机、是否机械套公式、主副互补）；先保证语义精确再压缩。

当前封面文案规则：`references/cover-copy-v6.md`。配套方法：`references/cover-value-method.md`、`references/title-review.md`。默认主标题≤15个汉字、副标题≤18个可见字素簇；主标题允许1–3行、副标题1–2行。标签与CTA独立核算，不设固定总字符数或跨类型主视觉面积比例；以完整封面缩略图和分享预览检查。

先运行 `tools/check_package.py`；读取 `assets/knowledge-locator.json` 后，使用 `scripts/cover_assets.py` 校验固定Manifest、查询并下载选中源资产。只下载本轮需要的记录，不扫描整仓。

标题门禁使用 `tools/cover_title_gate.py`；编辑评分使用 `tools/cover_review.py`；图片与最终ZIP用 `tools/check_image_export.py` 实测。每项状态只对实际验证范围负责。

本次不重建64款构图、17类结构、18套风格，不改变资产编号。

插画标题与笔记正文对照：`references/illustration-note-alignment-v1.json`，18篇（小红书6／抖音6／视频号6），含108条拍摄证据提示；只用于承诺兑现核对，不代表营销效果验证，也不授权改写原口播。
