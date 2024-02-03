from fastapi import FastAPI

app = FastAPI()


@app.get("/api/check")
def hello_world():
    return {"message": "Vortex is Running!"}
