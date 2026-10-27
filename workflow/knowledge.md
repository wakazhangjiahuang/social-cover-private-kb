# 资产路由 · v1.2.0

先读assets/knowledge-locator.json。目标wakazhangjiahuang/social-cover-private-kb允许公开；active表示已保存的固定版本通过读取与哈希抽查，不代表未来每次连接都成功。每次需要远程知识时，以manifest_ref完整提交SHA读取manifest_path，核对manifest_sha256；再读取所需资产及直接依赖并核对sha256。未实际读取的资产不称已使用或已全量验收。

manifest的资产ref若为完整SHA则使用该SHA；若为manifest_commit则继承消费者固定的manifest_ref。历史导出清单的export-v1.1.0-local-only只在locator明确绑定该历史导入提交时继承其固定SHA，不能拿导出标签代替远程版本。不得自动改账号或使用main的移动内容替代已固定提交。

按任务/行业/受众/目标→组件→公式/标题/钩子/布局/风格/证据取所需资产及直接依赖。manifest需id/path/tags/source/license/ref/sha256；不全仓扫描，不每次载入18类全文。用户225钩子、公式工作簿、双平台PDF都是候选结构；数字/亲测/稀缺/权威表达先查证据。平台机制、历史、作者主张与编辑建议分开；标题/钩子正文只维护一份，以ID引用。

远程可选资料失败时用本地短公式与当前素材继续并注明；必需品牌/证据缺失阻断对应步骤。公开仓库不代表其中资料获得公开使用许可；按实际source/license使用，不将当前私密输入自动写入公开库。新增经验经脱敏、真实回归与范围审核后，仅在用户授权范围写入。

知识库清单在其固定提交内描述资产；生产定位文件不列入其所定位清单，避免提交SHA/文件哈希循环自引用。已安装Skill的locator保存生产指针；仓库config/knowledge-locator.json供其他消费者读取同一已验证指针。更新资产后先验证新的固定内容提交，再更新定位文件，不直接追随main。

来源版本见assets/research-sources.json。仅研究未明确许可项目的链接，不复制其实现、模板或图片；Jev/Laya研究记录不是已接入服务。曝光分母、入口、版本或窗口不明时，不认定公式造成流量增长。GitHub连接可直接完成资料读取，无需cover_get_formulas等封面专用工具。
