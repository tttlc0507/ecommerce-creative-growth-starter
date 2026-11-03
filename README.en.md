# Ecommerce Creative Review

[中文](README.md) · v0.1.0 · MIT

Turn vague product-image feedback into specific, actionable revisions.

Give an image-capable AI assistant a product image, confirmed product details and the intended placement. The skill returns observations, prioritized copy-and-visual revisions, and a small test plan. It does not generate images, place ads, access seller accounts or predict performance lifts.

## Use

Clone this repository and copy `skills/ecommerce-creative-review` into the skill directory supported by your assistant. For a Codex project, use `.agents/skills/ecommerce-creative-review`. You can also ask the assistant to read `SKILL.md` directly.

```text
Use $ecommerce-creative-review to review this product image.
Product: name, variant, price and confirmed facts.
Placement: where the image will appear.
Goal: the problem we want to solve.
Prioritize actionable revisions and finish with a test card. Do not generate images.
```

Image review requires an assistant that supports images. Only format and local-tool checks were run in Codex; capabilities in other hosts depend on their integrations.

See the [fictional input](examples/demo-product.md), [original demo image](examples/demo-creative.svg) and [example review](examples/demo-review.md). They are demonstrations, not customer evidence or measured results.

## Optional metrics

Python 3.9+, standard library only:

```sh
python3 scripts/metrics.py examples/demo-metrics.csv
```

The script calculates descriptive CTR and CPC from raw counts. It does not calculate purchase CVR, choose a winner or perform causal analysis.

## Feedback and privacy

[Trial feedback](https://github.com/tttlc0507/ecommerce-creative-review/issues/new?template=trial-feedback.yml) · [Bug report](https://github.com/tttlc0507/ecommerce-creative-review/issues/new?template=bug.yml)

Issues are public. Do not post customer assets, account details, orders, private dashboards or credentials. Use fictional or authorized public examples. The repository has no upload service or telemetry; files submitted to your assistant remain subject to that assistant's and model provider's data policies.

## Development

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_release.py
```

## License

[MIT](LICENSE). The license covers files distributed in this repository.
