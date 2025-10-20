"""
Test Project - Einfache FastAPI Anwendung für Tests
"""

import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Test Project", version="1.0.0")


@app.get("/")
async def root():
    return {"message": "Hello World from Test Project"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
