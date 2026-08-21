import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager


if __name__ == "__main__":
    uvicorn.run("test:app", host="0.0.0.0", port=8000, reload=True)

@asynccontextmanager
async def mytest(app: "FastAPI"):
    print("Setting up test context...")
    yield
    print("Tearing down test context...")



app = FastAPI(title="My Test", description="Just for test", version="1.0.0", lifespan=mytest)

@app.get("/home/")
async def home():
    return {"message": "Welcome to My Test API!"}