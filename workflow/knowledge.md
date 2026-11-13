# 固定版本资产检索

1. 读取 `config/knowledge-locator.json`，取得完整 `manifest_ref` 与 `manifest_sha256`。locator是控制配置，不列入其定位的内容清单；正式消费者固定该提交，不自动追随main。
2. 从指定提交读取根 `manifest.json` 并核哈希。清单内 `ref=manifest_commit` 指继承该固定提交；按 entrypoints 和 `catalog/asset-groups.json` 选用途，再只读必要资产及依赖。
3. 封面选型先读17类信息结构，再查 `catalog/layout-index.json`。L01–L17、几何A–H、平台A/B/C和决策组件C01–C18是独立维度。按ID、结构、素材性质硬筛；主平台只作排序提示，明确 primary_only 才限制原主平台。
4. 实图调用前核 image.path、sha256、width、height、文件可读性和素材性质。64示例全部为AI合成人像，原场景生活化不等于真实摄影。未覆盖信息结构返回空结果，继续用本轮真实素材或原创设计。
5. 文字资料按 `record --kind component|hook|title|formula` 读取原文件和稳定ID；候选正文只维护原文件一份。225标题、225钩子、工作簿和PDF是用户候选／资料，不因入库而成为官方规则、真实案例或已验证爆款。
6. 历史规则来源见根 `sources.json`、`platform-audit.json` 和 `research-sources.json`。本次分类不重新认证其全部动态事实。涉及当前专项规则按任务重新核验。

GitHub代码搜索可能未建立索引，不能靠搜索空结果判断不存在。已知仓库直接读取固定 manifest→分类索引→选中记录；下载后可用 `tools/retrieve.py` 复现检索。参考原图暂不可取只阻断依赖该图的步骤，不停止无依赖创作。

`tools/validate_assets.py` 校验路径、PNG/JPEG完整解码、尺寸、唯一性、SHA256和HTML本地引用；`tools/tests/retrieval_test.py` 检查检索边界。结构与文件通过不代表成品营销效果或平台实机审核通过。

更新分两步：先提交并验证内容快照，再单独更新 locator 指向该快照，避免哈希循环。旧上传路径对应关系在 `catalog/path-migrations.json`；原始包清单与QA在 `sources/imports/cover64/`。公开仓库不改变许可，不自动写入本轮私密输入。
