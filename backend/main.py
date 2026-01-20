from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import ingest, items, query

app = FastAPI(title="AI Knowledge Inbox")

# ✅ CORS middleware (required for React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ingest.router)
app.include_router(items.router)
app.include_router(query.router)

@app.get("/")
def root():
    return {"message": "AI Knowledge Inbox API is running"}
