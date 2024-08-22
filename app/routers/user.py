
from sqlalchemy.orm import Session
from typing import   List
from fastapi import Depends,HTTPException , status , APIRouter
from .. import schemas , model
from .. import utils
from ..database import get_db


router = APIRouter(
    prefix="/users",
    tags = ['Users']
)

@router.get("/" , response_model = List[schemas.UserOut])
def display_users(db: Session = Depends(get_db)):
    user = db.query(model.User).all()
    if not user:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail = "no entries found"))
    return user

@router.post("/" , response_model = schemas.UserOut)
def create_user( user_prov : schemas.User ,db: Session = Depends(get_db)):
    user_prov.password = utils.get_password_hash(user_prov.password)
    try :
        user_data =model.User(**dict(user_prov))
        db.add(user_data)
        db.commit()
        db.refresh(user_data)
        return user_data
    except :
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE , detail = "User already exist ! Perhaps Try using another email !")


@router.get("/{id}" , response_model= schemas.UserOut)
def display_one_user( id : int , db: Session = Depends(get_db) ):
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION , detail= "No user found")

    return user


