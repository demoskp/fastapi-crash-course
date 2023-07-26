import uvicorn as uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

from api.views import api

load_dotenv()

app = FastAPI()


@app.get("/hello")
def hello():
    return {"hello": "world"}


app.include_router(api)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=9090,
        reload=True,
    )
