"""Rebuild delivery-intelligence state metrics from the three original Olist CSVs.

Usage: python analysis/rebuild_from_olist.py /path/to/olist-data --output state_metrics_rebuilt.json
Requires pandas; uses SQLite. Historical descriptive data, not causal inference.
"""
from __future__ import annotations
import argparse, json, sqlite3
from pathlib import Path
import pandas as pd

SQL = """
WITH items_per_order AS (
  SELECT order_id, COUNT(*) AS item_lines,
         SUM(price) AS merchandise_brl, SUM(freight_value) AS freight_brl
  FROM items GROUP BY order_id
), clean_orders AS (
 SELECT o.order_id, c.customer_state AS state,
   (julianday(o.order_delivered_customer_date) - julianday(o.order_purchase_timestamp)) AS delivery_days,
   CASE WHEN julianday(o.order_delivered_customer_date) <= julianday(o.order_estimated_delivery_date)
     THEN 1 ELSE 0 END AS ontime,
   MAX(0.0, julianday(o.order_delivered_customer_date) - julianday(o.order_estimated_delivery_date)) AS delay_days,
   COALESCE(i.item_lines,0) AS item_lines,
   COALESCE(i.merchandise_brl,0.0) AS merchandise_brl,
   COALESCE(i.freight_brl,0.0) AS freight_brl
 FROM orders o
 INNER JOIN customers c ON o.customer_id=c.customer_id
 LEFT JOIN items_per_order i ON o.order_id=i.order_id
 WHERE o.order_status='delivered'
   AND o.order_purchase_timestamp IS NOT NULL
   AND o.order_delivered_customer_date IS NOT NULL
   AND o.order_estimated_delivery_date IS NOT NULL
   AND o.order_purchase_timestamp != ''
   AND o.order_delivered_customer_date != ''
   AND o.order_estimated_delivery_date != ''
)
SELECT state, COUNT(*) AS orders, ROUND(100.0*AVG(ontime),3) AS on_time_pct,
       ROUND(AVG(delivery_days),3) AS avg_delivery_days,
       SUM(1-ontime) AS late_orders,
       ROUND(AVG(delay_days),3) AS avg_delay_all_days,
       ROUND(AVG(merchandise_brl),3) AS avg_order_merchandise_brl,
       ROUND(AVG(freight_brl),3) AS avg_freight_brl,
       SUM(item_lines) AS line_items
FROM clean_orders
WHERE delivery_days IS NOT NULL
GROUP BY state ORDER BY orders DESC
"""

def compute_metrics(orders: pd.DataFrame, customers: pd.DataFrame, items: pd.DataFrame) -> list[dict]:
    for table, df, col in [('orders', orders, 'order_id'), ('customers', customers, 'customer_id')]:
        if df[col].isna().any() or not df[col].is_unique:
            raise ValueError(f'{table} must have unique, nonnull {col}; joining would inflate counts')
    connection = sqlite3.connect(':memory:')
    try:
        orders.to_sql('orders', connection, index=False)
        customers.to_sql('customers', connection, index=False)
        items.to_sql('items', connection, index=False)
        metrics = pd.read_sql_query(SQL, connection)
    finally:
        connection.close()
    return metrics.to_dict(orient='records')

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_directory', type=Path)
    parser.add_argument('--output', type=Path, default=Path('state_metrics_rebuilt.json'))
    args = parser.parse_args()
    def load(stem): return pd.read_csv(args.csv_directory / f'olist_{stem}_dataset.csv')
    orders, customers, items = load('orders'), load('customers'), load('order_items')
    result = compute_metrics(orders, customers, items)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f'{len(orders):,} original orders; {len(result)} states; '
          f'{sum(x["orders"] for x in result):,} eligible delivered orders; saved {args.output}')

if __name__ == '__main__':
    main()
