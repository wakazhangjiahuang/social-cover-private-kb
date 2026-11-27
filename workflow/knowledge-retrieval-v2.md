# 知识检索与版本治理 V2.0

1. 先读取 config/knowledge-locator.json，固定 manifest_ref、manifest_sha256、inventory_sha256。
2. 从固定 commit 读取 manifest.json 并校验 SHA256；禁止浮动 main 回退。
3. 按 platform_mode、surface、任务阶段、QA gate 读取 entrypoint 和 dependencies。
4. 记录实际加载的来源 ID、版本、哈希、用途和状态。
5. 缺失、权限失败、哈希不符、来源过期时标 BLOCKED/UNKNOWN，不静默换历史资料。

状态：current_rule、official_source、academic_platform_paper、user_approved_reference、editorial_reference、candidate_requires_evidence、performance_verified、negative_regression、historical_only、superseded、unknown_needs_recheck。

非破坏式维护：保留有效资产和原始文件；历史资料只逻辑归档；新文件追加并更新 Manifest、Inventory、SHA256、README、Locator、测试和变更日志。
