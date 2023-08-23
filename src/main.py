import uvicorn
from fastapi import FastAPI

from auth.router import router as auth_router

app = FastAPI()


@app.get("/")
def health_check() -> dict[str, str]:
    return {"Health check": "OK"}


app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
