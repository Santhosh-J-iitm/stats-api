from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://dash-jq5e24.example.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_headers(request: Request, call_next):
    start = time.perf_counter()

    response = await call_next(request)

    process_time = time.perf_counter() - start

    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{process_time:.6f}"

    return response

@app.get("/stats")
def stats(values: str):
    numbers = [int(x) for x in values.split(",")]

    return {
        "email": "23f2002608@ds.study.iitm.ac.in",
        "count": len(numbers),
        "sum": sum(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "mean": sum(numbers) / len(numbers)
    }