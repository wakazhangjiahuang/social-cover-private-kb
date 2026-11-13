Social Cover Studio 真人封面校对版 0.3

1. 完整解压后打开 START.html；也可打开 index.html。
2. covers 内有64张独立PNG：小红书22套、抖音21套、微信视频号21套。不是64套各输出三平台。跨平台使用需按HTML审校改编。
3. 每套保留独立构图，真人为AI原创写实示例；并非实拍、客户见证或真实成效。正式发布须替换授权素材或保留AI来源并使用平台声明功能。
4. 规则事实、设计推断、证据缺口分开列出。未提供可核实的爆款数据，效果仍需账号验证。
5. covers.json为逐款规格与192项跨平台审校；64-cover-audit.csv便于表格筛选；sources.json与platform-audit.json记录规则范围与缺口；QA.json记录本地检查。
6. fonts为可再分发的Noto子集和许可。src/render.cjs可由装有@napi-rs/canvas与sharp的Node环境重建。直接看图和HTML不需要安装依赖或联网。
7. HTML交互未完成实际浏览器运行验证；可在不使用脚本时逐张查看图片及展开信息。下载按钮读取同包本地图片。
8. 本包未部署、未更新现有social-cover-studio插件。
