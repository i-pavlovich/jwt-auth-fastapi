import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def health_check() -> dict[str, str]:
    return {"Health check": "OK"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
