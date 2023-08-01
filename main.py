import uvicorn
from fastapi import FastAPI

from api.views import api

app = FastAPI()

app.include_router(api)


@app.get("/hello")
def hello():
    return {"hello": "world"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8080,
        reload=True
    )
