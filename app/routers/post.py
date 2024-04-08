
from sqlalchemy.orm import Session 
from typing import   List , Optional
from fastapi import Depends,HTTPException , status , Response , APIRouter 
from .. import schemas , model , oauth2
# from ..utils import verify_password , get_password_hash
from ..database import get_db
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags = ['Posts']
)

@router.post("/" , status_code= status.HTTP_201_CREATED , response_model=schemas.displayPosts)
# def posting(sample_post : posts ):
#     cursor.execute("""INSERT INTO postsdatas (title , post , content) VALUES (%s , %s,%s) RETURNING *""" , (sample_post.title , sample_post.post , sample_post.content))
#     new_data = cursor.fetchone()
#     conn.commit()   
#     return (new_data)
def posting(sample_posts :schemas.posts , db: Session = Depends(get_db) , user_id : int  = Depends(oauth2.get_current_user)):
    

    cache =model.post(**dict(sample_posts))
    db.add(cache)
    db.commit()
    db.refresh(cache)
    return cache

# response_model=List[schemas.displayPosts]
@router.get("/" , response_model = List[schemas.postOut])
def show_allposts(db: Session = Depends(get_db) , user_output : int = Depends(oauth2.get_current_user),
                  limit :int=20 ,skip :int = 0 , search : Optional[str] = "" ):
    # if len(postss)==0:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail = "No post has been created yet")
    # cursor.execute("""SELECT * FROM postsdatas """)
    # postss = cursor.fetchall()
    # print(postss)
    # return postss
    # print(type(user_output))
    # print(user_output.id)
    

    #without the voting(join functionality) feature
    # postsss = db.query(model.post).filter(model.post.title.contains(search)).limit(limit).offset(skip).all()

    #with the join feature
    results = db.query(model.post , func.count(model.Vote.post_id).label("votes")).join(model.Vote , model.Vote.post_id == model.post.id , isouter = True).group_by(model.post.id).filter(model.post.title.contains(search)).limit(limit).offset(skip).all()
    # print the number of votes
    return results


@router.get("/{user_id}", response_model = List[schemas.displayPosts])
def show_myposts(db : Session = Depends(get_db) , user_id : int = Depends(oauth2.get_current_user)):
    postss = db.query(model.post).filter(model.post.user_id == user_id).all()
    return postss




@router.get("/indi_post/{id}" , status_code=status.HTTP_302_FOUND, response_model = schemas.postOut)
def view_posts(id : int , response : Response , db: Session = Depends(get_db),current_user : int  = Depends(oauth2.get_current_user)):
        # response.status_code = status.HTTP_100_CONTINUE
        # try:
        #     cursor.execute("""SELECT * FROM postsdatas WHERE id = %s ;""" , (id,))
        #     returned_data = cursor.fetchone()

        #     return (returned_data)
        # except Exception as err:
        #     print("error is : " , err)
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail= "the entered data is not found in the database :/")
    # postt = db.query(model.post).filter(model.post.id == id).first()
    postt = db.query(model.post , func.count(model.Vote.post_id).label("votes")).join(model.Vote , model.Vote.post_id == model.post.id , isouter = True).group_by(model.post.id).filter(model.post.id == id).first()

    print(postt)
    if not postt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail = "the id has not been found")
    else:
        return postt
    

    
@router.delete("/{user_id}/{id}" , status_code=status.HTTP_200_OK)
def delete_postbyid(id : int, db: Session = Depends(get_db),user_id : int  = Depends(oauth2.get_current_user)):
    # try :
    #     cursor.execute("""DELETE FROM postsdatas WHERE id = %s RETURNING *;""" , (id,))
    #     deleted_post = cursor.fetchone()
    #     conn.commit()
    #     print("the post has been succesfully deleted")
    #     return("deleted post : ",deleted_post)
    # except Exception as err:
    #     print("the post with the mentioned id not found!")
    #     return("error: ",err)


    posttt = db.query(model.post).filter(model.post.id == id)
    if not posttt.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = "no post with id found")
    # print(posttt.first().user_id == int(user_id))
    if posttt.first().user_id != int(user_id):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "you are not allowed to delete someone else's post !")
    
    posttt.delete(synchronize_session=False)
    db.commit()
    return("post has been succesfully deleted")
    #else:
    #return ("you are not allowed to delete post created by someone else !")


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

    # try :
    #     cursor.execute("""UPDATE postsdatas SET title = %s ,
    #                    post = %s , content = %s where id = %s returning * ;""",(user_input.title,
    #                                                                               user_input.post,
    #                                                                               user_input.content,
    #                                                                               id))
    #     updated_post = cursor.fetchone()
    #     if updated_post==None:
    #         response.status_code=status.HTTP_404_NOT_FOUND
    #         return ("the post with the curresponding id does not exist")
    #     conn.commit()
    #     return ("updated post : ",updated_post)
    # except Exception as error:
    #     return error
    # user_input = user_input.model_dump()
