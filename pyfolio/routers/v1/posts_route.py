from typing import Union

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pyfolio.dependencies import get_db
from pyfolio.repositories.post_repository import PostRepository
from pyfolio.schemas.base_response_schema import SuccessResponse
from pyfolio.schemas.post_schema import PostCreate, PostUpdate

router = APIRouter()


@router.get("")
def read_posts(skip: int = 0, limit: int = 10, sort: str = 'id', order='desc',
               search_by: str = '', search_value: str = '',
               db: Session = Depends(get_db)):
    posts = PostRepository(db).paginate(
        skip=skip,
        limit=limit,
        sort=sort,
        order=order,
        search_by=search_by,
        search_value=search_value
    )
    return SuccessResponse(
        message='Retrieve posts successfully',
        data=posts
    )


@router.get("/{idOrSlug}")
def read_post(idOrSlug: Union[int, str], db: Session = Depends(get_db)):
    if isinstance(idOrSlug, str):
        post = PostRepository(db).find_by_slug(slug=idOrSlug)
    else:
        post = PostRepository(db).find(id=idOrSlug)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return SuccessResponse(
        message='Retrieve post successfully',
        data=post
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = PostRepository(db).find_by_slug(post.slug)
    if db_post:
        raise HTTPException(status_code=400, detail="Slug already exists")
    post = PostRepository(db).create(post)
    if post is None:
        raise HTTPException(status_code=500, detail="Failed to create post")
    else:
        return SuccessResponse(
            message='Created post',
            data=post
        )


@router.put("/{id}")
def update_post(id: int, post: PostUpdate, db: Session = Depends(get_db)):
    db_post = PostRepository(db).find(id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    post_data = post.dict(exclude_unset=True)
    print(post_data)
    for key, value in post_data.items():
        setattr(db_post, key, value)
    post = PostRepository(db).update(db_post)
    return SuccessResponse(
        message='Updated post',
        data=post
    )


@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    db_post = PostRepository(db).find(id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    PostRepository(db).delete(db_post)
    return {
        "message": "Post was deleted successfully."
    }
