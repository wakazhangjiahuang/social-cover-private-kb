# social-cover-private-kb｜V2.0 增量知识层

本目录是 V2.0 additive overlay，继承基础快照 `88cb7f6a68ef0710dc963f9ad35d172e9cd07c1f`，不替换、不删除、不移动任何既有资产。运行时读取本分支固定 overlay manifest 与 inventory；不得使用 floating main。

## 新增资产地图
- `platform-modes/A-H-platform-modes.md`：八平台入口、营销表达类型、文本职责、规格/合规边界。
- `copy-architecture/four-level-copy-v2.md`：主标题、副标题、补充文案、CTA 与主画面证据合同。
- `workflow/six-stage-pipeline-v2.md`：六阶段链路、三道总关口、失败回退和 A/B 模式。
- `evidence/platform-algorithm-and-rules-register.md`：平台公开算法机制、官方规则和未公开边界。
- `qa/qa-contract-v2.md`：事实、文本、视觉、平台、文件和独立验证门禁。
- `manifest-overlay.json` / `inventory-overlay.json`：新增文件入口、依赖、来源、SHA 与状态。

## 继承的基础资产
原 17 类结构、18 套风格、64 款构图、8 个几何家族、18 个模块/179 字段、V5.1 文案规则、用户认可样例和历史文件全部留在基础快照中。V2.0 不复制它们，也不重命名原 ID。

## 读取流程
1. 读取 `config/knowledge-locator-v2.0.json`。
2. 校验 base Manifest ref/SHA 与基础 Inventory SHA。
3. 校验本分支 Overlay Manifest/Inventory SHA。
4. 根据 platform_mode + surface 定向加载对应适配器，再加载文本合同、链路、证据或 QA。
5. 记录实际文件 ID、来源、版本、SHA、使用目的和状态。

## 非破坏式维护
禁止删除任何既有文件或资产。旧版通过 `historical_only`、`superseded_by`、`default_retrieval=false` 逻辑归档。新增资料只追加新路径与唯一 ID；原始资料、Prompt、图片、工作簿、历史规则保持原路径和原始字节。