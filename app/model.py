from sqlalchemy import TIMESTAMP, Column , Integer , Boolean , String, text , ForeignKey
from sqlalchemy.orm import relationship
# from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base


class post(Base):
    __tablename__ = 'postsdatas'

    id = Column(Integer , primary_key= True , nullable = False)   
    post = Column(Boolean , server_default='TRUE' , nullable= False)
    title = Column(String , nullable=False)
    content = Column(String , nullable = False)
    created_at = Column(TIMESTAMP(timezone=True) , nullable= False , server_default= text('now()'))
    user_id = Column(Integer , ForeignKey("userlogininfo.id" , ondelete="CASCADE") , nullable = False)
    owner  = relationship("User")
class User(Base):
    __tablename__ = "userlogininfo"

    id = Column(Integer , primary_key=True , nullable = False)
    password = Column(String , nullable = False)
    email = Column(String , unique= True ,nullable = False )
    created_at = Column(TIMESTAMP(timezone=True) , nullable= False , server_default= text('now()'))


class Vote(Base):
    __tablename__ = 'votes'

    user_id = Column(Integer , ForeignKey("userlogininfo.id",ondelete="CASCADE") ,primary_key=True, nullable = False)
    post_id = Column(Integer , ForeignKey("postsdatas.id",ondelete="CASCADE") , primary_key = True, nullable = False)
    
    



