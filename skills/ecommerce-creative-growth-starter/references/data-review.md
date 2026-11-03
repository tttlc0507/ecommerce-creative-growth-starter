# 数据输入与复盘

数据来自用户记录、导出表或实际接入的授权工具。本包不连接后台、不运行监控；链接和截图不授予账号权限。

## CSV 字段

必需表头：`creative_id,impressions,clicks,spend`。空值保留为未知，原始计数不能是百分比或公式。支持常见中文别名。每行是一条记录，不自动合并重复素材。

| 可选字段 | 意义 |
| --- | --- |
| channel,placement,audience,period | 渠道、位置、人群、日期／区间 |
| attribution_window | 实际归因窗口和规则，或明确不适用 |
| conversion_event,conversions | 转化事件名称及原始计数 |
| conversion_base_event,conversion_base_count | 分母事件名称及原始计数 |

`paid_buyers,6,visitors,120` 表示支付买家数／访客数；`add_to_cart_users,9,visitors,120` 表示加购人数／访客数，不能称为支付 CVR。名称来自用户确认，脚本不能核实平台实际记录是否匹配。

- CTR = clicks / impressions × 100%。须为同一统计范围。
- CPC = spend / clicks。沿用输入币种，不作换算。
- conversion_rate_pct = conversions / conversion_base_count × 100%，须分子、分母名称和计数齐备。
- cost_per_conversion = spend / conversions，须转化事件和计数齐备，解释时保留该事件名称。

缺失或 0 分母输出 null；正曝光下 0 点击的 CTR 为 0。仅有“CVR”列时不反推成交。缺事件定义时给待核对提示。

## 先检查，再解释

核对素材版本、日期、位置、人群、事件、花费、归因窗口和回补情况。不同来源或层级不直接混合，同素材重复行不自动汇总。

先陈述变化再列候选解释。CTR 上升而后续转化变弱，可能涉及受众、承诺与页面承接、价格或样本波动，不能只因一个比率更高就宣布优胜。详情页也可能更适合理解度或后续行为，不能拿主图 CTR 替代。

缺随机分流、可比条件或统计计划时，只作描述性复盘和下一轮建议。本脚本不检验显著性或自动定胜负；下一轮写明希望排除哪种解释。
