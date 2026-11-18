# 执行与规格协议
任务卡：平台、入口、受众、真实承诺、素材角色、锁定项、允许变化、数量、授权和停止点。视频证据带时间戳，参考特征分别标继承/改写/忽略/未知。
独立核查相关官方规则和任务资产，合并事实与约束后生成六案；每案自动作具体专业决定，不把设计参数全问给用户。构建6份CoverSpec，排除硬失败，再选3份；真实图像创作与验收另行执行。
结构约定见config/cover-spec.schema.json。单案含id/mode/topic/audience/promise/headline/subheadline/visual_route、evidence_refs、modules、elements、palette/rendering/constraints/crop_status/qa/production。modules完整覆盖C01–C18：id/status(apply|omit)/decision/params/qa；apply给具体参数，omit解释。elements含id/role/reference_id/copy/bbox/z_order/protected。evidence_refs含id/kind/source/role/allowed_transforms。
计划容器为schema_version=1.1.0、mode、concepts(默认6)、selected_ids(默认3，未选时空)、selection_reason、capabilities。用户数量优先，非默认明确requested_count。无字封面headline为空，C02–C05相应omit并解释。
六个独立选择轴：内容角度、主视觉路线、信息组织、绘制语言、颜色系统、文字处理。用户锁定的轴不改；六案在至少两个允许轴有实质不同。不是每次强制6种预设各一份。
共同约束：关键词/眼嘴/产品/证据优先于层次效果；证明区保持同口径且清楚；作品细节是卖点时让出标题；品牌色冲突先调局部承载；固定有限系列锚点而非三案同版；坐标是目标，不当实测。
关键主题或平台不明只补必要问题，材料不足不生成成绩/经历/认证/假截图。正文/发布请求交回对应工作流。


## 封面文案专用支线（V4）

当任务包含封面主副标题时，先按 `cover-copy/cover-copy-v4.md` 完成：事实卡 → 共同任务 → 具体观看收益 → 材料支持的入口 → 主标题/副标题/主画面合读 → 六项门禁。内部策划卡与四项工作指导不得搬上封面。标题任务内部比较2–3个实质不同入口即可；不得把视觉方向的“6案择优3案”机械套成标题生成数量。旧标题/钩子/公式候选不是默认模板。

## 插画标题—笔记正文对照样例

- 三平台18篇脚本（小红书6、抖音6、视频号6）及对应正文、锁定开场、Calling、发布文案和108条拍摄证据提示：`cover-copy/illustration-note-alignment-v1.json`。
- 插画封面任务按需读取；先检查标题承诺是否由正文/画面兑现。只优化封面时，不改写原口播、Calling或发布文案。
- 该文件是用户提供的脚本样例，不是效果数据；时长估算、自检分、案例标题均不代表真实CTR或爆款验证。
