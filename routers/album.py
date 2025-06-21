# routers/album.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import models.album as models
import schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/albums", response_model=schemas.AlbumOut)
def create_album(album: schemas.AlbumCreate, db: Session = Depends(get_db)):
    db_album = models.Album(**album.dict())
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album

@router.get("/albums", response_model=list[schemas.AlbumOut])
def list_albums(db: Session = Depends(get_db)):
    return db.query(models.Album).all()

@router.post("/photos", response_model=schemas.PhotoOut)
def add_photo(photo: schemas.PhotoCreate, db: Session = Depends(get_db)):
    db_photo = models.Photo(**photo.dict())
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo

@router.get("/albums/{album_id}/photos", response_model=list[schemas.PhotoOut])
def list_photos(album_id: int, db: Session = Depends(get_db)):
    return db.query(models.Photo).filter(models.Photo.album_id == album_id).all()
