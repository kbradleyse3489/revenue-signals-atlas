# Revenue Signals — ATLAS / Delivery Intelligence Lab

**Project 04 | Interactive e-commerce delivery analytics**

An interactive exploration of historical Brazilian e-commerce delivery patterns using the public Olist dataset (2016–2018). The application examines delivery timeliness, geography, freight costs, merchandise value, seller-to-customer corridors, and a hypothetical improvement scenario.

## Live experience

[Open ATLAS](https://keishawalker.tech/atlas/) · [Portfolio](https://keishawalker.tech)

## Technologies

Standalone HTML, CSS, and JavaScript with embedded visualization libraries and prepared historical aggregates. No application server, API key, or package installation is required.

## Findings and interpretation

The eligible sample contains 96,470 delivered orders, including 7,826 late deliveries (approximately 8.11%; 91.89% on time). The seller-to-customer panel describes 110,189 item lines across 412 state pairs. State rankings, monthly cohorts, and corridor comparisons reveal descriptive variation to investigate; they do not identify its causes. Use the linked state dossier and monthly view to inspect sample sizes before interpreting percentages.

## Dataset and methodology

Source: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). Original dataset terms and attribution apply.

The dashboard documents 99,441 unique orders joined to customer IDs, 96,478 delivered orders, and exclusion of eight delivered records without required timestamps. Item values and freight are aggregated to order grain before order-level comparisons. Delivery timeliness compares actual delivery against the original estimated date. Geographic markers use approximate state capitals. State confidence intervals express binomial sampling uncertainty; they do not adjust for dependence or differences in product mix.

## Run locally

This distribution is a standalone HTML dashboard. Open `index.html` in a modern browser. To serve it locally for testing:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`.

## Portfolio features

- Geographic exploration of delivery metrics by Brazilian state
- State-level detail and ranked comparisons
- Seller-to-customer state-pair network analysis
- Historical time-series views
- Explicit separation of observed metrics and hypothetical scenarios

## Method notes

- Historic Olist e-commerce data (2016–2018), not current delivery performance.
- Dashboard headline lists 96,470 date-valid, eligible delivered orders and 7,826 late deliveries.
- Seller-to-customer connections are item-level lines; they should not be interpreted as independent orders.
- Scenario analysis is hypothetical, not an observed business outcome or a validated causal forecast.
- This distribution includes the interactive visualization, not the original data-processing notebooks, SQL, or model training pipeline; do not claim those assets are present.

## Deployment

For a static host (GitHub Pages, Netlify, etc.), publish `index.html` as the site's entry point. If integrating into a larger portfolio, embed via a dedicated route or link to the published dashboard. Test mobile sizing, plots, and remote basemap availability after deployment.

## Attribution

Source: Brazilian E-Commerce Public Dataset by Olist, hosted on Kaggle. This is an independent portfolio project, not an official Olist dashboard.

## Limitations

The historical sample is not representative of current operations. Capital-to-capital distances are approximations, not measured shipping routes. Item-line late shares repeat an order-level flag and are not parcel failure rates. The time-series chart omits three tiny 2016 cohorts while national totals retain them. The improvement slider is illustrative, with no validated causal or forecasting model. Embedded aggregates enable exploration but are not a substitute for the original preparation pipeline.

## Interaction guide

Choose a geography signal and minimum order volume, then select a state marker or ranked bar. Adjust the hypothetical improvement slider to inspect its arithmetic scenario. Filter seller origins, corridor size, and network signal; select a lane for details or export displayed lanes to CSV. Inspect historical monthly cohorts and read the Method section for grain and scope.
