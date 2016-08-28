# Small Business Cashflow management

## Objective: To create an adaptive cashflow forecasting tool for small business to better manage working capital

Beginning balance + cashflow over time period = ending balance
  - Users can see projection by day, week, month

1. Cashflow projection (Worst case scenario): Customers pay at the last possible due date
  - Cashflow is projected based on the final invoice due date

2. Cashflow projection (updated real time based on bank cashflows)
  - Calls are made to USBank to check if invoices are paid ahead of due date
      - Transactions are matched based on amount and description 
      - Cashflow calculations are updated based on confirmation of invoice payment
  - Calls are made to USBank to check if invoices are late
      - Cashflow calculations are updated

3. Invoice Issuance
  - Using Mastercard API issue invoices and create invoice records
  
4. Invoice Review
  - Using Mastercard API, call a list of invoices for be review by the small business owners
  
5. Loan (collateralized)
  - Using outstanding loans to act as collaterals for potential small business loans.

  




