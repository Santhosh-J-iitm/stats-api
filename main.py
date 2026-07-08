from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import yaml
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Default configuration
config = {
    "port": 8000,
    "workers": 1,
    "debug": False,
    "log_level": "info",
    "api_key": "default-secret-000",
}

# Load YAML layer
if os.path.exists("config.development.yaml"):
    with open("config.development.yaml", "r") as f:
        data = yaml.safe_load(f)
        if data:
            config.update(data)

# Helper to convert to boolean
def to_bool(value):
    return str(value).lower() in ["true", "1", "yes", "on"]

# Load .env layer
if os.getenv("APP_PORT"):
    config["port"] = int(os.getenv("APP_PORT"))

if os.getenv("NUM_WORKERS"):
    config["workers"] = int(os.getenv("NUM_WORKERS"))

if os.getenv("APP_DEBUG"):
    config["debug"] = to_bool(os.getenv("APP_DEBUG"))

if os.getenv("APP_API_KEY"):
    config["api_key"] = os.getenv("APP_API_KEY")

# Load OS environment variables (highest before CLI)
if os.getenv("APP_WORKERS"):
    config["workers"] = int(os.getenv("APP_WORKERS"))

if os.getenv("APP_LOG_LEVEL"):
    config["log_level"] = os.getenv("APP_LOG_LEVEL")

if os.getenv("APP_PORT"):
    config["port"] = int(os.getenv("APP_PORT"))

if os.getenv("APP_DEBUG"):
    config["debug"] = to_bool(os.getenv("APP_DEBUG"))

if os.getenv("APP_API_KEY"):
    config["api_key"] = os.getenv("APP_API_KEY")


@app.get("/effective-config")
def effective_config(set: list[str] = Query(default=[])):
    result = config.copy()

    # CLI overrides
    for item in set:
        if "=" not in item:
            continue

        key, value = item.split("=", 1)

        if key in ("port", "workers"):
            result[key] = int(value)
        elif key == "debug":
            result[key] = to_bool(value)
        else:
            result[key] = value

    # Never expose the real API key
    result["api_key"] = "****"

    return result