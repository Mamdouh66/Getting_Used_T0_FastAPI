from fastapi import FastAPI

app = FastAPI()

@app.get('/', tags= ['Root'])
async def root() -> dict:
    return {'message' : 'Hello World'}


@app.get('/todo', tags=['todos'])
async def get_todo() -> dict:
    return {'data': todos}

@app.post('/todo', tags = ['todos'])
async def add_todo(todo:dict) -> dict:
    todos.append(todo)
    return {'data' : 'todo added successfully'}

@app.put('/todo/{id}', tags= ['todos'])
async def update_todo(id: int, body: dict) -> dict:
    for todo in todos:
        if int((todo['id'])) == id:
            todo['Activity'] = body['Activity']
            return {'data' : f'todo with {id} has been updated successfully'}
        
    return {'data' : f'todo with {id} not found'}
         
@app.delete('/todo/{id}', tags= ['todos'])
async def delete_todo (id: int) -> dict:
    for todo in todos:
        if int((todo['id'])) == id:
            todos.remove(todo)
            return {'data' : f'todo with {id} has been deleted successfully'}
        
    return {'data' : f'todo with {id} not found'}

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