from fastapi import FastAPI

app = FastAPI()

@app.get('/', tags= ['Root'])
async def root() -> dict:
    return {'message' : 'Hello World'}


@app.get('/todo', tags=['get list of todos'])
async def get_todo() -> dict:
    return {'todos', todos}


todos = [
    {
     "id" : 1,
     "Activity" : "Go to class"   
    },
    {
     "id" : 2,
     "Activity" : "Meet with Ali"   
    }
]