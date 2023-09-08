from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models, hashing
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()
    
models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog', status_code = status.HTTP_201_CREATED, tags=['Blogs'])
async def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body, user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Blogs'])
async def delete_blog(id,  db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id ({id}) was not found')
    
    blog.delete(synchronize_session = False)
    db.commit()
    return {'details' : 'Blog was deleted successfully!!!'}

@app.put('/blog/{id}', status_code = status.HTTP_202_ACCEPTED, tags=['Blogs'])
async def update_blog(id, request: schemas.Blog,  db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id ({id}) was not found')
    
    blog.update(request)
    db.commit()
    return {'details' : 'updated succesfully'}

@app.get('/blog', response_model = List[schemas.GetBlog], tags=['Blogs'])
async def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code = status.HTTP_200_OK, response_model = schemas.GetBlog, tags=['Blogs'])
async def get_blog(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Blog with {id} was not found')
    
    return blog

@app.post('/user', response_model=schemas.GetUser, tags=['Users'])
async def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name = request.name, email = request.email, password = hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}', response_model=schemas.GetUser, tags=['Users'])
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f'User with {id} was not found')
    
    return user