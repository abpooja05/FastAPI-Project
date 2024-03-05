from fastapi import FastAPI, HTTPException, Query, Depends, BackgroundTasks
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker,declarative_base, relationship, Session
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

import time  # Import the time module

from uvicorn import Config, Server
from app import app  # Replace 'main' with the actual name of your FastAPI app module

if __name__ == "__main__":
    config = Config(app=app)
    server = Server(config)
    server.run()
# FastAPI app
app = FastAPI()

# Database connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy base
Base = declarative_base()


# Database models
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    publication_year = Column(Integer)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    text = Column(String)
    rating = Column(Integer)

    book = relationship("Book", back_populates="reviews")


Book.reviews = relationship("Review", back_populates="book")

# Create tables
Base.metadata.create_all(bind=engine)


# Pydantic models
class BookBase(BaseModel):
    title: str
    author: str
    publication_year: int

    class Config:
        json_schema_extra  = ConfigDict(title='The title of the book', author='The author of the book', publication_year='The publication year of the book')


class BookCreate(BookBase):
    title: str
    author: str
    publication_year: int


class BookUpdate(BookBase):
    title: Optional[str] = None
    author: Optional[str] = None
    publication_year: Optional[int] = None


class BookDB(BookBase):
    id: int

    class Config:
        from_attributes = True


class ReviewBase(BaseModel):
    text: str
    rating: int

    class Config:
        json_schema_extra = {
            "description": "The base model for a review",
            "example": {
                "text": "Example Review Text",
                "rating": 5
            }
        }


class ReviewCreate(ReviewBase):
    book_id: int


class ReviewUpdate(ReviewBase):
    text: Optional[str] = None
    rating: Optional[int] = None


class ReviewDB(ReviewBase):
    id: int
    book_id: int

    class Config:
        from_attributes = True


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Background task to send email
def send_confirmation_email(email: str, review_text: str):
    # Simulate sending email (sleep for 5 seconds)
    print(f"Sending confirmation email to {email} for review: {review_text}")
    time.sleep(5)
    print("Email sent")


# Endpoints for CRUD operations
# Function to retrieve books records from the database
@app.get("/books/", response_model=List[BookDB])
def get_books(author: Optional[str] = None, publication_year: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Book)
    if author:
        query = query.filter(Book.author == author)
    if publication_year:
        query = query.filter(Book.publication_year == publication_year)
    return query.all()


# Function to add a new record in the database
@app.post("/books/", response_model=BookDB)
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


# Function to update an existing record in the database
@app.put("/books/{book_id}", response_model=BookDB)
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for attr, value in book.dict().items():
        setattr(db_book, attr, value)
    db.commit()
    db.refresh(db_book)
    return db_book


# Function to delete a record from the database
@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted"}


# Function to retrieve reviews records from the database
@app.get("/reviews/{book_id}", response_model=List[ReviewDB])
def get_reviews(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book.reviews


# Function to add a new record in the database
@app.post("/reviews/", response_model=ReviewDB)
def submit_review(review: ReviewCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_review = Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    # Start background task to send confirmation email
    background_tasks.add_task(send_confirmation_email, "abpooja05@gmail.com", review.text)
    return db_review


# Function to update an existing record in the database
@app.put("/reviews/{review_id}", response_model=ReviewDB)
def update_review(review_id: int, review: ReviewUpdate, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    for attr, value in review.dict().items():
        setattr(db_review, attr, value)
    db.commit()
    db.refresh(db_review)
    return db_review


# Function to delete a record from the database
@app.delete("/reviews/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(db_review)
    db.commit()
    return {"message": "Review deleted"}







