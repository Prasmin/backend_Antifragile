from fastapi import FastAPI 

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World", "message": "I am creating a FastAPI application!"}