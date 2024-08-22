from fastapi import FastAPI , status
from .database import engine
from . import model
from .routers import post , user , auth , vote
from . Config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.get("/" , status_code=status.HTTP_302_FOUND)
def welcomescreen():
    return "welcome to the Interactive API !!!"

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
        







