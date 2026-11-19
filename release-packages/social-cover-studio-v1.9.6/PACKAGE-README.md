# social-cover-studio v1.9.6｜完整独立包

本压缩包包含两部分：

1. `01-skill/social-cover-studio/`：从 ChatGPT 插件当前正式发布版读取的完整 Skill 目录，保留 SKILL.md、agents、assets、config、evals、references、release、requirements、scripts、tools 等全部文件。
2. `02-knowledge-base/`：构建时从本仓库固定提交复制的完整知识库快照，包含64款构图图、64张缩略图、18套风格参考图与预设、结构/风格索引、规则、来源和校验清单。

## 版本与来源

- Skill：social-cover-studio 1.9.6
- Plugin release：pluginrel_6afdefbac9a481918d7a5166179b1308
- Knowledge base repository：wakazhangjiahuang/social-cover-private-kb
- Knowledge base source branch：main（本次构建对应提交见构建日志及压缩包内 GitHub snapshot 文件）
- 本包不替代已安装的 ChatGPT 插件；它是供独立部署、审查和备份的完整 Skill + 知识库归档。

## 目录

- `01-skill/social-cover-studio/SKILL.md`：Skill 主入口
- `01-skill/social-cover-studio/references/`：完整规则、平台适配、标题案例、证据契约
- `01-skill/social-cover-studio/tools/` 与 `scripts/`：检查、评分、资产检索和导出工具
- `01-skill/social-cover-studio/evals/`：回归样例与测试
- `02-knowledge-base/`：独立知识库镜像，含原始资产及索引

## 安装提示

Codex 项目级安装：将 `01-skill/social-cover-studio/` 复制到项目的 `.agents/skills/social-cover-studio/`。
Codex 全局安装：将该目录复制到 `$CODEX_HOME/skills/social-cover-studio/`（如使用默认路径，按本机 Codex 配置确定 Skills 目录）。

知识库运行时仍按 Skill 内 `assets/knowledge-locator.json` 指向的固定 GitHub 快照执行远程完整性校验和按需资产读取；`02-knowledge-base/` 是随包备份与离线审查镜像，不会自动改写运行时定位配置。

## 事实与验证边界

- 包含全部 Skill 目录文件；构建前按插件当前发布版逐个读取。
- 包含知识库仓库快照；64款构图和18套风格素材按仓库原始文件保存。
- 4张温泉封面正向样例在 Skill 的 JSON 中保留文案、字符数与哈希记录；原始透明PNG未纳入本包，避免把参考图误当作生产素材。
- 29/29自动化测试结果来自 v1.9.6 已记录的测试报告；本次打包会另行执行 ZIP 完整性与文件数量校验，不把打包校验说成真实平台效果验证。
