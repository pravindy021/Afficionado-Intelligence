# Methodology

## Revenue

Revenue is the sum of `transaction_qty * unit_price`. It is sales value, not profit.

## Product segmentation

Products are compared against median units sold and median revenue.
Stars have above-median revenue and units; Premium Performers have above-median revenue;
Volume Drivers have above-median units; remaining products are Underperformers.
These rules are transparent thresholds and do not imply causal business recommendations.

## Unsupported analyses

`transaction_id` is unique to each source row, so there is no evidence that it represents a
complete customer basket. Basket mining is therefore not performed. Product cost and operating
expense fields are absent, so profitability cannot be calculated.

## Transaction and revenue counting

Transaction count uses `nunique(transaction_id)`. In the source workbook, every transaction ID
occurs on exactly one row, so this is the source-supported transaction count. Revenue is sales
value, not profit. Average transaction value sums derived revenue by unique transaction ID before
taking the mean.

## Pareto and ABC analysis

Products are ranked by revenue descending. Cumulative revenue share determines class: A through
80%, B through 95%, and C for the remainder. These are configurable descriptive rules, not
invented demand or profit classes.

## Date coverage

The source has a `year` and `transaction_time` field but no calendar date. It supports 2025 and
hour-of-day aggregation only. It does not support valid 7, 14, or 30-day date forecasts.
