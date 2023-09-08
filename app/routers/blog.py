from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from .. import schemas, models, database, models

router = APIRouter()
get_db = database.get_db

@router.get('/blog', response_model = List[schemas.GetBlog], tags=['Blogs'])
async def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.post('/blog', status_code = status.HTTP_201_CREATED, tags=['Blogs'])
async def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body, user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Blogs'])
async def delete_blog(id,  db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id ({id}) was not found')
    
    blog.delete(synchronize_session = False)
    db.commit()
    return {'details' : 'Blog was deleted successfully!!!'}

@router.put('/blog/{id}', status_code = status.HTTP_202_ACCEPTED, tags=['Blogs'])
async def update_blog(id, request: schemas.Blog,  db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id ({id}) was not found')
    
    blog.update(request)
    db.commit()
    return {'details' : 'updated succesfully'}

@router.get('/blog/{id}', status_code = status.HTTP_200_OK, response_model = schemas.GetBlog, tags=['Blogs'])
async def get_blog(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Blog with {id} was not found')
    
    return blog
