# Small Business Cashflow management

## Objective: To create an adaptive cashflow forecasting tool for small business to better manage working capital

Beginning balance + cashflow over time period = ending balance

1. Cashflow projection (Worst case scenario): Customers pay at the last possible due date

  - Cashflow is projected based on the final invoice due date
  - Users can see projection by day, week, month

2. Cashflow projection (updated real time based on bank cashflows)

  - Calls are made to USBank to check if an invoices are paid ahead of due date
      - Transactions are matched based on amount and description 
  - Cashflow calculations are updated based on confirmation of invoice payment
  




