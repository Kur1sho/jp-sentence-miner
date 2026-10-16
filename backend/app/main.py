from fastapi import FastAPI

app = FastAPI(title="Sentence Miner API")


@app.get("/health")
def health():
    return {"status": "ok"}