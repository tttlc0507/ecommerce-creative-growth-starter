# Ecommerce Creative Growth

[中文](README.md) · v0.2.1 · MIT

Connect product facts and performance data to creative briefs, artwork reviews, test plans and the next iteration. For ecommerce operations and design teams using an AI assistant that supports `SKILL.md`.

The basic cycle: inputs → diagnosis and focused research → selling-point hypotheses and copy/visual brief → artwork review → user-run test → data review → next action and learning record. Enter at the relevant stage. Historical data is optional for a new product.

Supports listing images, multi-section product detail pages and ad creatives. These placements need different criteria and outcome metrics. Copy and visuals develop together. Users create the artwork and run campaigns.

## Use

Copy `skills/ecommerce-creative-growth-starter` into your assistant's skill directory. Codex projects can use `.agents/skills/ecommerce-creative-growth-starter`, or ask the assistant to read `SKILL.md` directly.

```text
Use $ecommerce-creative-growth-starter for this product project.
Product facts: variant, price, confirmed features and sources.
Current task: research, brief, artwork review, test plan or data review.
Placement: listing image, detail page or ad creative.
Goal and attachments: images/versions; optional raw counts and context.
Separate facts, hypotheses and results. Deliver the next action.
Do not generate images or place ads.
```

Image review needs an image-capable host. Links do not grant seller-account access. Supply text, ordered screenshots and exports; this repository includes no platform integration or background monitoring.

## Local metrics

Python 3.9+, standard library:

```sh
python3 scripts/metrics.py examples/demo-metrics.csv
```

Calculates descriptive CTR, CPC and optional explicitly defined conversion metrics. A column called CVR alone is insufficient. See [fields and interpretation](skills/ecommerce-creative-growth-starter/references/data-review.md). No aggregation, winner selection or causal analysis.

[Examples](examples/demo-cycle.md) are fictional, not customer evidence or measured product benefits. No performance lifts are promised.

## Feedback and privacy

[Trial feedback](https://github.com/tttlc0507/ecommerce-creative-growth-starter/issues/new?template=trial-feedback.yml) · [Bug report](https://github.com/tttlc0507/ecommerce-creative-growth-starter/issues/new?template=bug.yml)

Issues are public. Use fictional or authorized public material; do not post customer assets, business data, dashboards, orders or credentials. No upload service or telemetry is included. Material supplied to an AI assistant is processed under that host's and model provider's data settings.

## Checks and license

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_release.py
```

[MIT](LICENSE), covering only the files distributed here. Format and local tools have been checked; business impact has not been established.
