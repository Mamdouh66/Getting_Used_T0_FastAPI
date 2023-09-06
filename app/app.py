from fastapi import FastAPI

app = FastAPI()

@app.get('/', tags= ['Root'])
async def root() -> dict:
    return {'message' : 'Hello World'}