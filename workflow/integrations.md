# 能力接入
实际发现工具并真实请求，安装不代表依赖已连通。初始状态见assets/integration-status.json；不伪造端点、概率或调用。
GitHub：真实读取固定manifest和代表资产，验证private/ref/hash；401/403/404不等于仓库不存在。必需资产失败阻断依赖步骤。
Laya：优先多语言、固定运行时代码与权重revision，每案必要摘要做choice/score/noul原子判断，允许弃权，长文本拆分。Jev：有真实服务/版本/认证才调用，JevHarness不是模型或凭据。
无决策服务可明确主模型复核，Jev/Laya接入验收仍未通过。answer_confidence与熵类confidence不混用；中文任务阈值需校准，不预设0.8通行。高置信不是正确率，文本模型不看像素。Cloudflare Worker不能直接容纳约GB级Laya权重，使用独立运行时/已有服务。
NoteRx：用户报告原项目已接入；新Skill核对实际工具、图片覆盖、版本、字段。仅C模式补充，不当A/B官方规则源，不代替看图。
GPT Image：官方已核实gpt-image-2.5-sunburst及gpt-image-2.5-sunburst-2026-09-08。https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst ; https://developers.openai.com/api/reference/resources/images/methods/generate ; https://developers.openai.com/api/docs/guides/image-prompting 。quality按任务，max不代替验收。
宿主工具无model参数不能靠Prompt锁2.5。宿主能可靠报告实际型号时按宿主imagegen规范执行；否则用已验证适配器或保留Prompt/规格，明确生图阻断。不绕过宿主图片工具限制。官方API凭据走受保护配置，不在聊天索取或在包/GitHub/日志存密钥。
托管插件的外部模型配置来自受保护服务端设置；默认未配置即返回明确缺口，不提供占位服务地址。参考图须确实传入，不能以文字描述冒充图像参考。
