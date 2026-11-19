# Deployment

## Windows development

```powershell
.\venv\Scripts\python.exe -m pip install -r backend\requirements.txt
$env:PYTHONPATH="backend"
.\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --app-dir backend
cd frontend
npm install
npm run dev
```

## Docker

```powershell
docker compose up --build
```

Services:
- Backend: port 8000
- Frontend: port 5173 through development compose configuration

Set production secrets only through environment variables. Do not place secrets in the frontend or workflow files.
