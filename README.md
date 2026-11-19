# social-cover-studio v1.9.6｜完整独立压缩包

本包是完整的 Skill + 知识库归档，不是增量补丁。

## 包含内容

- `01-skill/social-cover-studio/`：从 ChatGPT 插件当前正式发布版读取的全部 Skill 文件（67个），包括 SKILL.md、agents、assets、config、evals、references、release、requirements、scripts、tools。
- `02-knowledge-base/`：`wakazhangjiahuang/social-cover-private-kb` 当前 main 源码快照（239个文件），包括64款构图原图、64张缩略图、18套风格图片与预设、17类结构分类、索引、元数据、规则、证据和完整校验清单。

## 版本来源

- Skill：`social-cover-studio 1.9.6`
- ChatGPT Plugin ID：`Plugin_e4230c540f8481919e2832b93092bf1c`
- Plugin Release：`pluginrel_6afdefbac9a481918d7a5166179b1308`
- Knowledge Base 原始提交：`6273cb723263d5662717710e867dd2bbc4ae4c89`
- 本压缩包的GitHub分支：`package/social-cover-studio-v1.9.6-standalone`

## 目录说明

- Skill入口：`01-skill/social-cover-studio/SKILL.md`
- 启动提示：`01-skill/social-cover-studio/assets/START-PROMPTS.md`
- 标题规则：`01-skill/social-cover-studio/references/cover-copy-v6.md`
- 温泉正向样例：`01-skill/social-cover-studio/references/hot-spring-positive-cases-v2.json`
- 插画18篇对照：`01-skill/social-cover-studio/references/illustration-note-alignment-v1.json`
- 64款构图和18套视觉风格原始资产：`02-knowledge-base/covers/`, `02-knowledge-base/thumbs/`, `02-knowledge-base/styles/`

## 安装方式

**Codex项目级：** 将 `01-skill/social-cover-studio/` 复制到项目的 `.agents/skills/social-cover-studio/`。

**Codex全局：** 将该目录复制到 `$CODEX_HOME/skills/social-cover-studio/`（具体位置以本机Codex Skills配置为准）。

**知识库：** `02-knowledge-base/` 是随包保存的完整本地镜像。当前Skill中的 `assets/knowledge-locator.json` 仍按v1.9.6原始设计固定指向GitHub知识库提交，用于远程完整性校验和按需读取；离线镜像用于备份、迁移和审查，不会自动改写远程定位器。

## 边界说明

- 本包包含完整Skill目录和完整知识库文件快照。
- 四张温泉正向样例的原始透明PNG未嵌入Skill；其文案、字符计数、来源哈希和使用边界保存在V2 JSON中。
- 包内已有29/29自动化测试通过记录；本次压缩归档不代表真实目标用户盲测、平台发布预览或CTR效果验证。
- 本包是Skill和知识库源文件归档，不包含ChatGPT插件的宿主端运行环境或任何第三方平台账户授权。
