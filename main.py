from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, session_local
from sqlalchemy.orm import Session


app = FastAPI()
models.base.metadata.create_all(bind=engine)

class Record_Base(BaseModel):
    tittle: str
    content: str
    user_id: int

class User_Base(BaseModel):
    username: str
    first_name: str
    second_name: str

def get_db():
    db = session_local()
    try:
        yield db
        
    finally:
        db.close()

db_dependecy = Annotated[Session, Depends(get_db)]


@app.post('/records/', status_code=status.HTTP_201_CREATED)
async def create_record(record: Record_Base, db: db_dependecy):
    db_record = models.Record(**record.dict())
    db.add(db_record)
    db.commit()

@app.get('/records/{record_id}', status_code=status.HTTP_200_OK)
async def read_record(record_id: int, db: db_dependecy):
    record = db.query(models.Record).filter(models.Record.id == record_id).first()
    if record is None:
        raise HTTPException(status_code=404, detail='Запис не знайдено')
    return record

@app.delete('/records/{record_id}', status_code=status.HTTP_200_OK)
async def delete_record(record_id: int, db: db_dependecy):
    db_record = db.query(models.Record).filter(models.Record.id == record_id).first()
    if db_record is None:
        raise HTTPException(status_code=404, detail='Запис не знайдено')
    db.delete(db_record)
    db.commit()


@app.put('/records/{record_id}', status_code=status.HTTP_200_OK)
async def update_record(record_id: int, record:Record_Base, db: db_dependecy):
    db_record = db.query(models.Record).filter(models.Record.id == record_id).first()
    if db_record is None:
        raise HTTPException(status_code=404, detail='Запис не знайдено')
    db.query(models.Record).filter(models.Record.id == record_id).update(record.dict(), synchronize_session=False)
    db.commit()



@app.post('/users/', status_code=status.HTTP_201_CREATED)
async def create_user(user: User_Base, db: db_dependecy):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()

@app.get('/users/{user_id}', status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependecy):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='Користувача не знайдено')
    return user


@app.delete('/user/{user_id}', status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: db_dependecy):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='Запис не знайдено')
    db.delete(db_user)
    db.commit()

@app.put('/user/{user_id}', status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user:User_Base, db: db_dependecy):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='Запис не знайдено')
    db.query(models.User).filter(models.User.id == user_id).update(user.dict(), synchronize_session=False)
    db.commit()

