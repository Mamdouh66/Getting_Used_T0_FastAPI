from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from .. import schemas, models, database, models
from ..repository import blog

router = APIRouter(
    prefix = '/blog',
    tags = ['Blogs']
)

get_db = database.get_db

@router.get('/', response_model = List[schemas.GetBlog])
async def get_blogs(db: Session = Depends(get_db)):
    return blog.get_all(db)

@router.post('/', status_code = status.HTTP_201_CREATED)
async def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.create(db, request)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(id: int,  db: Session = Depends(get_db)):
    return blog.delete(id, db)

@router.put('/{id}', status_code = status.HTTP_202_ACCEPTED)
async def update_blog(id, request: schemas.Blog,  db: Session = Depends(get_db)):
    return blog.update(id, request, db)

@router.get('/{id}', status_code = status.HTTP_200_OK, response_model = schemas.GetBlog)
async def get_blog(id: int, db: Session = Depends(get_db)):
    return blog.get(id, db)
