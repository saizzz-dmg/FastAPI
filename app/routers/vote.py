from fastapi import Depends,HTTPException , status , Response, APIRouter 
from ..database import get_db
from .. import oauth2 , model
from sqlalchemy.orm import Session

from .. import schemas

router = APIRouter(
    prefix = "/vote",
    tags = ["VOTES"]
)

@router.post("/", status_code = status.HTTP_201_CREATED)
def voting(vote : schemas.Vote , db :Session = Depends(get_db) , current_user :int = Depends(oauth2.get_current_user)):
    vote_check = db.query(model.post).filter(vote.post_id == model.post.id).first()
    vote_query = db.query(model.Vote).filter(vote.post_id == model.Vote.post_id , current_user == model.Vote.user_id)
    if not vote_check:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail = "no post with such id found !")
    if vote_query.first():
        if vote.vote_dir:
            raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED , detail = 'post has already been upvoted')
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return "successfully downvoted"
    else:
        if vote.vote_dir:
            cache = model.Vote(**{"post_id" :vote.post_id,
                                  "user_id" : current_user })
            db.add(cache)
            db.commit()
            return "succesully voted:)"
        else:
            raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED , detail = 'already downvoted!')
        
        



        