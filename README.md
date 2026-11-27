# 自媒体封面资产库 · V2.0 知识体系

机器读取从根 manifest.json 开始；固定快照与哈希见 config/knowledge-locator.json。默认只读取执行索引与命中条目，不扫描整个仓库。inventory.json 是完整文件校验清单，不是创作知识索引。

## 平台适配
A 抖音、B 微信视频号、C 小红书、D 闲鱼、E 淘宝/天猫、F 抖音商城、G 抖音电商直播、H 淘宝直播。入口与营销类型见 platforms/README-v2.md。

## 现有视觉资产（全部保留）
18 套视觉风格；17 类语义结构；64 款构图、8 个几何家族；18 个决策模块、179 个字段。现有图片、缩略图、Prompt、工作簿和检索工具保持原样。64 款构图只覆盖 17 类中的 8 类；无图匹配时使用本轮素材原创排版，不伪称存在匹配模板。

## V2.0 当前执行入口
指导书摘要：guides/social-cover-studio-v2.0/README.md
平台适配：platforms/README-v2.md 与 A–H 独立文件
四级文本合同：workflow/cover-expression-contract-v2.md
六阶段链路：workflow/pipeline-contract-v2.md
检索与治理：workflow/knowledge-retrieval-v2.md
QA：workflow/qa-v2.md
平台证据：research/platform-evidence-2026-11-27.json

## 文案边界
A/B/C 继续 V5.1 主标题≤12、副标题≤18 可见字素簇默认预算；D–H 不继承该预算。补充文案与 CTA 可为空。平台算法公开资料不是封面独立权重或 CTR 公式。

## 检索与测试
运行 tools/retrieve_v2.py verify；按 platform --mode H、stage --id 03、gate --id G1、source --id XHS-SEARCH-KDD26 定向检索。原有 tools/retrieve.py、validate_assets.py 和 Node 测试继续保留。

## 版本与非破坏式维护
V4/V5/V6 等历史文件保留；V5.1 是 A/B/C 当前文案规则。旧版通过状态和替代关系逻辑归档，不删除。新增文件必须登记 Manifest、Inventory、SHA256、检索索引、变更日志和回归测试。详细规则见 maintenance/non-destructive-maintenance-policy-v2.md。
