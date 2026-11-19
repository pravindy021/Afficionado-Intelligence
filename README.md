# Afficionado Intelligence

Afficionado Intelligence is a modular retail analytics platform built with FastAPI and React.

## Current phase

The initial executive overview, product ranking, and dataset profile are functional.

## Windows setup

```powershell
.\venv\Scripts\python.exe -m pip install -r backend\requirements.txt
cd frontend
npm install
npm run dev
```

In a second terminal:

```powershell
$env:PYTHONPATH="backend"
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --app-dir backend
```

Open http://localhost:5173.

## Data limitation

The source workbook contains 149,116 rows and 11 columns. It has no cost, profit, inventory,
customer, or complete-order identifier fields. Each `transaction_id` appears once, so basket
analysis is disabled. Revenue is defined only as `transaction_qty * unit_price`.

## Analytics implemented

The platform now provides reusable core metrics, product and category ranking, store
performance, revenue contribution, hourly source-time trends, Pareto and ABC analysis,
product search/filtering, and dataset version/profile reporting.

Run the backend tests:

```powershell
$env:PYTHONPATH="backend"
.\venv\Scripts\python.exe -m pytest tests\backend -q
```
