# 18款风格的选择与调用

风格是视觉语言，结构是信息组织，构图是具体空间关系，平台是分发入口，组件是决策字段。不能把18模块称18风格，也不能把64构图称64风格。

1. 先完成本轮平台、受众、内容承诺与证据判断，再选择风格。读取固定清单中的visual_styles入口；用户点名风格ID时精确定位，不用模糊关键词替代。
2. 按选中记录读取一款 `styles/presets/{id}.json`、`styles/images/{id}.jpg` 与metadata对应键，校对preset_sha256、image.sha256。只检索索引不写成已看图。无执行器时直接用授权GitHub按固定ref读取。
3. 原图用于观察文字层级、色彩关系、边框、图文遮挡、人物与留白。完整原Prompt保留供理解，但其中原人物、身份、品牌、文案、亲测或结果不进入当前任务事实。引用图不提供真实客户或实拍证据。
4. metadata中的配色、字体和布局为INFERRED编辑提示，不证明原字体文件或全部视觉判断准确。源Prompt的文字面积、阴影等数值不是平台硬规则；与本轮保真、可读性或用户约束冲突时重排并说明采用的抽象关系。
5. 原来源平台为小红书；跨抖音或视频号时只迁移视觉语言，标题、首帧关系、比例与裁切按本轮平台适配器重新决定。没有当前客户端实测不称发布审核通过。
6. `joint`返回所选风格与对应信息结构的构图候选；没有实例时保留风格、按结构原创设计。联合结果不等于现成组合图或真实效果验证。

18款ID：background-big-text、cozy-home、dark-glow、dashed-decoration、hand-drawn-border、home-motivation、multi-layer-layout、neon-contrast、outdoor-handwriting、pink-yellow-playful、professional-clean、professional-woman、split-screen-tags、sticker-energy、study-room-intellectual、thinking-question、workplace-big-text、yellow-pink-banner。
