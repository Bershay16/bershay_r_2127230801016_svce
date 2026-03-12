# NVD CPE API

## How to run

1. Install dependencies
```bash
pip install -r requirements.txt
```

2. Load the data into the database
```bash
.venv/bin/python3 -m app.ingest
```

3. Start the server
```bash
.venv/bin/python3 -m uvicorn main:app --reload
```

## Endpoints

```
GET /api/cpes?page=1&limit=10
GET /api/cpes/search?cpe_title=apache
```