# 自媒体封面资产库 · 基础资产 v1.4.0 / 当前执行层 V2.0

> 当前 Skill 执行入口：`config/knowledge-locator-v2.0.json`。它固定引用基础资产快照与 V2.0 增量 Overlay；平台模式为 A–H。根目录 `manifest.json` 和 `config/knowledge-locator.json` 仅代表保留的基础快照，不应单独视为完整的当前平台路由。


机器读取从根 `manifest.json` 开始；固定提交与哈希见 `config/knowledge-locator.json`。默认只读执行索引与选中记录，不扫描整个仓库。\`inventory.json\` 是完整文件校验清单，不是创作知识索引。

| 层 | 数量 | 唯一内容入口 |
|---|---:|---|
| 视觉风格 | 18 | `catalog/style-index.json` → `styles/presets/`、`styles/images/` |
| 信息结构 | 17类 | `catalog/layout-family-taxonomy.json` |
| 构图实例 | 64，8种几何家族 | `catalog/layout-index.json` → `covers/`、`thumbs/` |
| 基础平台模式 | A抖音／B视频号／C小红书 | 基础快照历史入口；当前 A–H 八平台执行规则见 `v2.0/README.md` 与 `config/knowledge-locator-v2.0.json` |
| 决策框架 | 18模块、179字段 | `cover-components.json`，按C01–C18引用 |
| 标题／钩子／公式候选 | 225／225／10 | `titles/candidates.json`、`hooks/candidates.json`、`formulas/core-formulas.json` |

这六层不是同一种分类。风格可与结构和构图组合；组合是规划参考，不代表已有18×64套成品。64款实际覆盖17类中的8类，未覆盖结构返回无图匹配并使用本轮素材原创排版。

## 检索

```bash
python3 tools/retrieve.py style --id hand-drawn-border
python3 tools/retrieve.py style --query '手绘 边框'
python3 tools/retrieve.py joint --style-id neon-contrast --structure L05 --platform C
python3 tools/retrieve.py layout --id A01
python3 tools/retrieve.py record --kind component --id C01
python3 tools/validate_assets.py
python3 -m unittest discover -s tools/tests -p '*_test.py'
node --test tools/tests/core.test.mjs
```

查询使用独立命名空间和明确字段；代码搜索未收录不表示素材不存在。18张风格原图和64张PNG保持原始字节；调用时按固定清单校对SHA256。图片完整性校验需Pillow，检索仅用Python标准库。

风格原Prompt逐字保留在各自preset中；配色、字体与布局映射在 `styles/metadata.json` 标明INFERRED，不能当精确字体识别或官方平台规则。原图的人物、文案、身份与效果不直接迁移。64款构图使用AI合成人像，不是实拍、客户或真实案例证据。

## 原始资料与维护边界

`sources/originals/`、完整提取稿、`sources.json`、`platform-audit.json`和`research-sources.json`保留来源与日期，仅在任务确需时加载，默认执行索引不收录其长篇正文。未核实数字、平台红线和经验公式不能自动升级为规则。重复的模块拆分、工作簿分表、缺源码的应用配置和过期报告已删除，清理明细见 `maintenance/cleanup-report.json`；历史版本仍可从提交历史取回。

根 `START.html` 保留64款图集；上传的V5离线工作台原件保存在 `workbench/START.html`，供参考查看，不是在线服务。两份HTML及渲染源码不进入默认知识检索。 `src/`与`fonts/`用于可选重建；不自动安装应用或部署服务。

## 当前封面文案规则｜V5.1（2026-11-24）

封面主副标题采用独立执行标准：
- 当前规则：`cover-copy/cover-copy-v5.1.md`，以最新交付的V5.1 Word指导书为准。
- 主标题默认≤12个可见字素簇，副标题≤18个可见字素簇；英文、数字、空格、标点和Emoji均计入，换行不计。
- 新创作/重大重写内部比较三种实质不同的入口；简单润色和锁定文案不强制重跑。
- 以共同任务、观看回报、证据、主副表达契约和内容兑现为核心；执行G1–G7门禁。
- 评分仅用于定位短板，不作为候选排名或发布放行；编辑、盲读、平台预览和真实效果分开记录。
- V6/V5/V4保留为历史参考。15组插画标题、四张温泉认可参考和18篇正文对照不自动构成事实或效果证明。
- 不重建现有视觉系统：17类结构、18套风格、64套构图、三平台资产和检索流程保持不变。

## 插画标题—笔记正文对照样例

- 三平台18篇脚本（小红书6、抖音6、视频号6）及对应正文、锁定开场、Calling、发布文案和108条拍摄证据提示：`cover-copy/illustration-note-alignment-v1.json`。
- 插画封面任务按需读取；先检查标题承诺是否由正文/画面兑现。只优化封面时，不改写原口播、Calling或发布文案。
- 该文件是用户提供的脚本样例，不是效果数据；时长估算、自检分、案例标题均不代表真实CTR或爆款验证。
