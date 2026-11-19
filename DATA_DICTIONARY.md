# Data Dictionary

| Column | Type | Description |
|---|---|---|
| transaction_id | integer | Source row transaction identifier |
| year | integer | Transaction year |
| transaction_time | time | Source transaction time |
| transaction_qty | integer | Units in the source row |
| store_id | integer | Store identifier |
| store_location | string | Store location |
| product_id | integer | Product identifier |
| unit_price | decimal | Recorded unit price |
| product_category | string | Product category |
| product_type | string | Product type |
| product_detail | string | Product name/detail |

`revenue` is derived as `transaction_qty * unit_price`.

## Derived fields

| Column | Formula or rule |
|---|---|
| revenue | `transaction_qty * unit_price` |
| revenue_share | Product/category/store revenue divided by total revenue |
| quantity_share | Group quantity divided by total quantity |
| cumulative_revenue_share | Running total of Pareto-ranked product revenue share |
| abc_class | A through 80%, B through 95%, C thereafter |
| hour | First two characters of `transaction_time`, 00-23 |
