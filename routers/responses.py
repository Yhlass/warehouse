from fastapi import *
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import *
from sqlalchemy.orm import *
from db import get_db
import crud
from models import responsesSchema, Responses
from typing import Optional

responses_router = APIRouter()

@responses_router.post('/add-responses')
def add_responses(req:responsesSchema, db: Session = Depends(get_db)):
    try:
        result =crud.create_response(req, db)
        result = jsonable_encoder(result)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong')


@responses_router.get('/get-responses')
def get_responses(
    request_id: Optional[int] = None,
    db: Session = Depends(get_db)):
    try:
        result =crud.read_responses(request_id, db)
        result = jsonable_encoder(result)
        return JSONResponse(status_code=status.HTTP_200_OK, content=result)
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong')
    
@responses_router.put('/update-responses/{id}')
def update_responses(id: int, req: responsesSchema, db: Session = Depends(get_db)):
    try:
        result = crud.update_responses(id, req, db)
        result = jsonable_encoder(result)
        return JSONResponse(status_code=status.HTTP_200_OK, content=result)
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong')

