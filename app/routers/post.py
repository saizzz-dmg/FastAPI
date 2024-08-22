
from sqlalchemy.orm import Session 
from typing import   List , Optional
from fastapi import Depends,HTTPException , status , Response , APIRouter 
from .. import schemas , model , oauth2
from ..database import get_db
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags = ['Posts']
)

@router.post("/" , status_code= status.HTTP_201_CREATED , response_model=schemas.displayPosts)
def posting(sample_posts :schemas.posts , db: Session = Depends(get_db) , user_id : int  = Depends(oauth2.get_current_user)):
    
    sample_posts = dict(sample_posts)
    sample_posts['user_id'] = user_id
    cache =model.post(**dict(sample_posts))
    db.add(cache)
    db.commit()
    db.refresh(cache)
    return cache


@router.get("/" , response_model = List[schemas.postOut])
def show_allposts(db: Session = Depends(get_db) , user_output : int = Depends(oauth2.get_current_user),
                  limit :int=20 ,skip :int = 0 , search : Optional[str] = "" ):
    results = db.query(model.post , func.count(model.Vote.post_id).label("votes")).join(model.Vote , model.Vote.post_id == model.post.id , isouter = True).group_by(model.post.id).filter(model.post.title.contains(search)).limit(limit).offset(skip).all()
    return results


@router.get("/{user_id}", response_model = List[schemas.displayPosts])
def show_myposts(db : Session = Depends(get_db) , user_id : int = Depends(oauth2.get_current_user)):
    postss = db.query(model.post).filter(model.post.user_id == user_id).all()
    return postss




@router.get("/indi_post/{id}" , status_code=status.HTTP_302_FOUND, response_model = schemas.postOut)
def view_posts(id : int , response : Response , db: Session = Depends(get_db),current_user : int  = Depends(oauth2.get_current_user)):
    postt = db.query(model.post , func.count(model.Vote.post_id).label("votes")).join(model.Vote , model.Vote.post_id == model.post.id , isouter = True).group_by(model.post.id).filter(model.post.id == id).first()

    print(postt)
    if not postt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail = "the id has not been found")
    else:
        return postt
    

    
@router.delete("/{user_id}/{id}" , status_code=status.HTTP_200_OK)
def delete_postbyid(id : int, db: Session = Depends(get_db),user_id : int  = Depends(oauth2.get_current_user)):



    posttt = db.query(model.post).filter(model.post.id == id)
    if not posttt.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = "no post with id found")

    if posttt.first().user_id != int(user_id):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "you are not allowed to delete someone else's post !")
    
    posttt.delete(synchronize_session=False)
    db.commit()
    return("post has been succesfully deleted")


@router.patch("/{id}" , status_code= status.HTTP_200_OK  , response_model= schemas.displayPosts)
def update_post(id :int, user_input : schemas.Updateposts , db: Session = Depends(get_db),user_id : int  = Depends(oauth2.get_current_user)):
    
    posttt = db.query(model.post).filter(model.post.id == id)
    print(posttt.first())
    print(posttt)
    if not posttt.first():
        raise HTTPException(status_code= status.HTTP_204_NO_CONTENT , detail = "no post with id found")
    
    posttt.update(dict(user_input) , synchronize_session=False)
    db.commit()
    new = db.query(model.post).filter(model.post.id == id).first()
    
    return (new)

