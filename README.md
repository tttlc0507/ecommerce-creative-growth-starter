# 电商创意增长助手

[English](README.en.md) · v0.2.2 · MIT

**用单品资料和表现数据，把运营的问题变成设计任务，再把测试结果变成下一轮动作。**

给电商运营、设计师和商家的 AI Skill。覆盖商品主图、详情页及投放素材，协助资料整理、问题诊断、卖点假设、图文任务、成稿审查、测试计划和结果复盘。用户负责制作和投放。

## 可以从哪一步开始

| 你手里有 | 助手帮助交付 |
| --- | --- |
| 商品文字、截图或链接 | 产品事实、资料缺口、需要调研的问题 |
| 现有素材与表现报表 | 数据口径核对、问题线索、验证方向 |
| 产品与需求线索，准备做图 | 购买理由假设，以及相互配合的文案和画面任务 |
| 做好的主图、详情页或投放图 | 实际看图反馈、修改优先级、版本记录 |
| 准备测试或已返回结果 | 测试卡、有限的数据结论、下一轮动作与经验记录 |

按当前阶段进入，无需每次从头重走。没有历史数据也能从商品资料开始。

## 安装与使用

这是给支持 `SKILL.md` 的 AI 助手使用的技能包，不是独立网站。识图、读表与联网能力由宿主决定；本地指标脚本使用 Python 3.9+，无需安装依赖。

```sh
git clone https://github.com/tttlc0507/ecommerce-creative-growth-starter.git
```

将 `skills/ecommerce-creative-growth-starter` 复制到宿主支持的技能目录。Codex 项目可用 `.agents/skills/ecommerce-creative-growth-starter`；也可以直接让助手读取该目录的 `SKILL.md`。[Codex 官方技能说明](https://learn.chatgpt.com/docs/build-skills)

```text
使用 $ecommerce-creative-growth-starter 继续这个单品项目。
商品资料：名称、规格价格、已确认的特点；可附详情截图或商品链接。
当前阶段：调研／图文任务／成稿审查／测试／数据复盘。
素材与位置：主图、详情页或投放图；已知渠道和目标人群。
目标：本轮希望解决的问题。
附件：现有素材与版本；如有数据，附原始计数、日期、渠道及口径。
请区分事实与假设，给本轮交付和下一步。不要生图或自动投放。
```

链接读不到时用文字、截图继续；商品链接不等于后台权限。数据可手工提供、导出 CSV 或由实际授权的工具取得，本仓库不自带平台连接器或监控服务。

## 可反复使用的流程

**资料与数据输入 → 问题诊断与必要调研 → 购买理由及图文任务 → 成稿回传 → 用户测试 → 结果回传 → 下一轮与经验记录。**

文案和画面共同表达购买理由。测试前明确对照、变化与固定条件；可以验证整套图文，也可以控制条件验证具体变化。

| 场景 | 审查与验证重点 |
| --- | --- |
| 主图／列表图 | 商品与购买信息识别、缩略展示；同一展位定义下的点击表现 |
| 详情页／多屏长图 | 信息顺序、购买理由与证明、异议回应；理解、加购或成交等实际事件 |
| 投放图／广告素材 | 受众与场景、行动目标、落地页承接；点击成本和可用后续行为 |

详情长图按屏序上传，报告只覆盖实际看到的部分；不同类型不套同一个分数，也不全部用 CTR 评价。

## 数据如何帮助决策

- 先核对日期、事件、位置、人群、花费和归因窗口，再看指标。
- 根据原始计数计算 CTR、CPC；自定义转化率须明确分子、分母事件和计数，单有“CVR”列不代表支付转化。
- 将变化写成问题线索与候选解释，再给验证动作。例如点击上升而后续行为变弱，需要检查流量变化、表达承诺与页面承接，不能直接认定素材更好。
- 形成“保留／修改／复测／补数据”建议及依据，记录适用条件。价格、人群、素材同时改变后的差异，不能全部归因给设计。

```sh
python3 scripts/metrics.py examples/demo-metrics.csv
```

脚本本地逐行计算，不自动分组、不选赢家、不作显著性或因果分析。[数据字段与复盘说明](skills/ecommerce-creative-growth-starter/references/data-review.md)

可从 [CSV 空模板](skills/ecommerce-creative-growth-starter/assets/metrics-template.csv) 整理自己的数据。[字段与计算示例](examples/metrics-walkthrough.md) 使用合成数字解释工具输出，不作为设计案例或效果证明。

## 边界与反馈

通过项目记录、交接和测试复盘支持持续优化。运营负责价格、预算、库存、受众和投放决策，设计师负责实际制作。

不生图、不自动投放、不抓取后台、不自带数据同步。没有上传服务或遥测；交给 AI 助手的素材按所选宿主与模型服务的数据设置处理。

[试用反馈](https://github.com/tttlc0507/ecommerce-creative-growth-starter/issues/new?template=trial-feedback.yml) · [报告问题](https://github.com/tttlc0507/ecommerce-creative-growth-starter/issues/new?template=bug.yml) · [贡献说明](CONTRIBUTING.md)

GitHub Issue 公开可见，只用虚构或有权公开的内容，不上传客户素材、真实经营数据、订单、后台截图或密钥。希望了解：交付能否直接用、是否减少运营与设计来回沟通、是否愿意完成下一轮。

## 检查与许可

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_release.py
```

按 `release-manifest.json` 发布。[MIT](LICENSE) 仅适用于本仓库实际分发的文件。已检查格式和本地工具，尚无本产品的真实业务增效证据。
