
from sqlalchemy.orm import Session
from typing import   List
from fastapi import Depends,HTTPException , status , Response , APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm 
from .. import schemas , model , database , oauth2
from ..utils import get_password_hash , verify_password

router = APIRouter(
    tags = ['Authenticator']
)

@router.post("/login" , status_code = status.HTTP_202_ACCEPTED , response_model = schemas.Token )
def login_validator(user_input : OAuth2PasswordRequestForm = Depends() , db: Session = Depends(database.get_db)):
    user = db.query(model.User).filter(user_input.username == model.User.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail = "Invalid Credentials")
    
    if not verify_password(user_input.password , user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail = "Invalid Credentials")
    
    access_token = oauth2.create_access_token(data = {'user_id' : user.id })
    # print(type(user.id))
    # return {"your access token : ": access_token , "token_type":"bearer"}
    return {"access_token" : access_token ,"token_type" : "bearer"}




    


