from fastapi import FastAPI

app = FastAPI(title="OpsGuard")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
