# 自媒体封面设计知识库 · v1.2.0

目标仓库：wakazhangjiahuang/social-cover-private-kb。用户已批准公开可见；可见性不改变各资产source/license所规定的使用范围。

## 已启用的流程

按任务读取固定版本的组件、标题、钩子与公式→当前模型回查证据、标题承诺与方案差异→包内脚本检查结构和几何→宿主图像工具创作→逐图核字、看图与裁切验收。保留18模块、179字段、六案择三与独立成品交付。

封面专用MCP、Jev与Laya已移出默认依赖；NoteRx仅在实际可用时补充C模式诊断。未发现可用服务时直接执行核心流程。图像默认不要求验证精确型号；未暴露时记录not_exposed并继续，不冒称具体版本。

## 固定版本与完整性

config/knowledge-locator.json保存active状态、manifest_ref完整提交SHA与manifest_sha256。用该提交读取manifest.json，并从同一提交读取ref=manifest_commit的资产，逐项校验sha256；不用移动分支main替代固定提交。

定位文件属于控制配置，不列入其所定位manifest或SHA256SUMS.txt，避免SHA和文件哈希循环自引用。先保存内容快照，再验证并更新定位文件；已安装Skill的定位配置与此文件使用同一内容指针。清单资产哈希只覆盖被索引内容，不等于已全量人工验收。

## 内容与运行

- components/、cover-components.json：18模块、179字段。
- hooks/、titles/：各225条用户候选及工作簿候选公式。
- formulas/、presets/、marketing/、body/：结构、表达和正文候选。
- sources/、research/：用户材料与来源、许可研究记录。
- workflow/、config/、integrations/：执行规范与保存的能力配置。
- examples/、templates/、tools/：样例、模板、校验与编译脚本。

在仓库根目录可运行node tools/cover_core.mjs capabilities读取保存的配置；validate、compile、delivery通过--input JSON路径使用；node --test tools/tests/core.test.mjs验证本轮规则。capabilities不是实时网络或模型服务探测。

公式与标题不构成已证实的爆款规律；数字、亲历、效果、权威、稀缺与对比必须匹配真实材料。没有真实图片不能称已成图，结构通过不代表语义或画面验收通过。当前私密输入不自动写入公开仓库。
