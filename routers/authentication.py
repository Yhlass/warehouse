from fastapi import *
from fastapi. requests import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBearer
from sqlalchemy import *
from sqlalchemy.orm import *
from db import get_db
import crud
from models import registerSchema, loginSchema, userSchema

authentication_router = APIRouter()

@authentication_router.post('/sign-in')
def sign_in(req: loginSchema,db: Session= Depends(get_db)):
    try:
        result = crud.signIn(req, db)
        if result:
            result =jsonable_encoder(result)
            return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=result)
        else:
            return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE, content={'result': 'Failed to login'})
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong')

@authentication_router.get('/user')
def get_user(department_id, position_id, db: Session = Depends(get_db)):
    try:
        result = crud.read_user(department_id, position_id, db)
        result = jsonable_encoder(result)
        return JSONResponse(status_code=status.HTTP_200_OK, content=result)
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong')
    

@authentication_router.post('/new-user')
def new_user(req: userSchema, db: Session = Depends(get_db)):
    try:
        result = crud.create_new_user(req, db)
        if result:
            result = jsonable_encoder(result)
            return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'result': 'User already exists'})
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"result": 'Something went wrong'})
    
@authentication_router.put('/delete-user/{id}')
def delete_user(id:int, db: Session = Depends(get_db)):
    try:
        result = crud.delete_user(id, db)
        result = jsonable_encoder(result)
        return JSONResponse(status_code = status.HTTP_200_OK, content=result)
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = 'Something went wrong')
     
