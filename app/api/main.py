from fastapi import FastAPI
import models
from database import engine
import uvicorn

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Api Online!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3005)
