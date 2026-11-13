# 自媒体封面设计知识库 · v1.3.0

唯一机器入口为 [`manifest.json`](manifest.json)，固定版本定位见 [`config/knowledge-locator.json`](config/knowledge-locator.json)。本仓库当前公开可见；公开访问不改变各文件的来源和使用许可。

## 已核实资产与分类

| 内容 | 数量 | 标准入口 |
|---|---:|---|
| 独立PNG与缩略图 | 64＋64 | `covers/{xhs,douyin,channels}/`、`thumbs/` |
| 逐款检索、哈希、尺寸、语义结构 | 64 | `catalog/layout-index.json` |
| 信息结构分类 | 17类 | `catalog/layout-family-taxonomy.json` |
| 原有决策框架 | 18模块、179字段 | `components/`、`cover-components.json` |
| 标题／钩子候选 | 各225条 | `titles/`、`hooks/` |
| 原始公式 | 10条 | `formulas/core-formulas.json` |
| 原始资料、提取稿和历史导入证据 | 分来源保存 | `sources/` |
| 执行规范与来源登记 | 按用途保存 | `workflow/`、`research/`、`sources.json`、`platform-audit.json` |

64款包含小红书22款、抖音21款、视频号21款；不是64款各有三平台成品。全部使用AI合成人像，包含看似工作室与户外的场景，不能当作实拍、客户或业绩证据。17类结构均保留；64款实际覆盖其中8类，缺失的9类不硬塞图片。

几何构图A–H、平台模式A/B/C、信息结构L01–L17、决策模块C01–C18分别检索，禁止混用编号。原示例主平台只作适配提示，不禁止将布局重排用于其他平台。

## 精确检索

```bash
python3 tools/retrieve.py layout --id A01
python3 tools/retrieve.py layout --platform C --structure L05
python3 tools/retrieve.py layout --family H --query '工作室 负空间'
python3 tools/retrieve.py layout --nature REAL_PHOTO
python3 tools/retrieve.py record --kind component --id C01
python3 tools/retrieve.py record --kind hook --id user-hook-001
python3 tools/validate_assets.py
python3 -m unittest discover -s tools/tests -p '*_test.py'
node --test tools/tests/core.test.mjs
```

`REAL_PHOTO`或未覆盖结构返回空匹配，并引导使用本轮真实素材／原创设计；不会用合成图补成真实证据。查询词按空格分组且全部需要匹配；精确编号、结构、家族和素材性质优先。GitHub代码搜索可能尚未索引，空结果不代表素材不存在。

按 [`workflow/knowledge.md`](workflow/knowledge.md) 读取固定提交清单、索引和选中的资产，核对SHA256。无需全库扫描或封面专用MCP。下载完整仓库后可离线打开 `START.html`；GitHub文件页面本身不运行HTML。重建脚本在 `src/`，需另备其声明的依赖；本轮未重绘原PNG。

本轮修复目录与索引，并核对文件、尺寸、哈希和结构分类；未验证当前平台客户端裁切或账号流量效果。历史平台资料仍按原日期与证据状态使用。原始导入声明保存在 `sources/imports/cover64/`，不当作本轮测试结果。
