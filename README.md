# 自媒体封面设计私有资产库 · v1.1.0

建议在 wakazhangjiahuang 账号创建 **Private** 仓库，统一命名 **social-cover-private-kb**。
插件源码建议另用 **social-cover-studio**，上传插件源码包 source/ 内文件。两个仓库承担不同用途。

## 上传方法

1. 解压本 ZIP，打开 social-cover-private-kb/。
2. 在新私有仓库选择 Add file → Upload files，把该文件夹里面的文件和子文件夹上传到仓库根目录。不要只把 ZIP 上传，也不要再套一层同名目录。可用 Git 客户端保留目录及 .gitignore。
3. 确认根目录可见 README.md、manifest.json、cover-components.json、hooks/、titles/ 等，提交后提供仓库链接。
4. 授权 GitHub 连接访问该私库。读取成功并固定版本、核对文件哈希后，才可将知识定位状态从 pending_access 改成 active。上传本身不会自动激活 Skill 或插件的远程知识读取。

## 分类内容

| 目录 | 内容 |
| --- | --- |
| components/、cover-components.json | 18模块、179字段、决策、验收和失败回路 |
| hooks/ | 225条用户钩子候选、工作簿钩子公式 |
| titles/ | 225条用户标题候选及工作簿标题公式 |
| formulas/、presets/ | 10种原创结构候选、工作簿封面结构 |
| marketing/、body/ | 人性机制、跨类型/B端表达和正文结构候选 |
| sources/ | 用户原始TXT/XLSX/PDF及已提取内容 |
| workflow/、platforms/ | 三平台路由、素材理解、设计、生成和验收协议 |
| research/、research-sources.json | 相关GitHub项目、固定版本与许可边界 |
| config/、integrations/ | 规格Schema、目标仓库定位、依赖实际状态 |
| examples/、templates/、tools/ | 规划样例、资产/案例记录模板、结构校验工具 |

## 使用原则

按任务→模块→标题/钩子/公式→直接依赖按需检索；不每次把全仓资料塞入Prompt。公式和标题是候选表达，不构成已证实的爆款或算法规则。数字、亲测、稀缺、权威、效果与对比先核实。

配置与记录里的空 ref/fixed_ref 表示尚无实际远程提交，不能编造版本。原材料中的“80%”“4.6倍”等说法未在本任务验证，不作为排序权重或承诺。没有导入未明确许可的项目实现、NoteRx可执行包、Jev凭据或Laya权重。

## 使用 Skill

将独立 Skill ZIP 导入目标账号支持的技能安装入口；无导入入口时，可上传 ZIP 并明确要求安装包内 social-cover-studio Skill。安装后在新对话调用“使用自媒体封面设计工作室，C模式，根据我的素材规划六案、择优三案”。精确模型与外部判断仍需各账号单独配置和验收。

本包整理日期：2026-10-27。manifest.json 与 SHA256SUMS.txt 用于核对解压内容；不是远程激活凭证。
