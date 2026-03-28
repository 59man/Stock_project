NOT FINISHED

project/
│── backend/
│   ├── main.py
│   ├── routers/
│   ├── services/
│   ├── db/
│── frontend/
│   ├── index.html
│   ├── add_asset.html
└── shared/




Backend

FastAPI

httpx or requests (for APIs)

pydantic (for data validation)

sqlite3 or SQLModel

Frontend

Pure HTML + JS
OR optional upgrade:

htmx (super simple dynamic UI!) — big boost without complexity.

Charts (optional)

Chart.js

User → adds asset → Frontend → sends request → FastAPI endpoint
→ saves to SQLite → fetches price → returns response → shown on HTML page






source venv/bin/activate.fish
