from jose import jwt , JWTError
from datetime import datetime , timedelta
from . import schemas
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends , HTTPException , status
from . import Config

#SECRETKEY
#ALOGORITHM
#EXPIRATIONTIME

SECRET_KEY = Config.settings.database_secretkey
ALGORITHM = Config.settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = Config.settings.SECRET_CODE_EXPIRATION_IN_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() +timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})

    encoded_jwt = jwt.encode(to_encode , SECRET_KEY , algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token :str , credentials_exception):

    try : 
        payload = jwt.decode(token , SECRET_KEY ,algorithms=[ALGORITHM])
        got_id: str = payload.get("user_id")
        # print(type(got_id))

        if not got_id:
            raise credentials_exception
        token_data = schemas.Tokendata(id=str(got_id))
    except JWTError:
        raise credentials_exception
    # print(token_data)
    return token_data.id


def get_current_user(token : str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED ,
                                           detail="Not Authorized" , headers={"WWW-Authenticate" : 
                                           "Bearer"})
    
    token = verify_access_token(token , credentials_exception)
    return token
    
    

        




