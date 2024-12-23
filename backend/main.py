from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (or specify a list of allowed origins)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def read_root():
    return {"message": "CORS is enabled!"}

# Database Configuration
DATABASE_URL = "postgresql://postgres:root@localhost/lv"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Model
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(255), nullable=True)
    main_cat = Column(String(255), nullable=True)
    sub_cat = Column(String(255), nullable=True)
    brand = Column(String(255), nullable=True)
    model = Column(String(255), nullable=True)
    housing_size = Column(String(255), nullable=True)
    function = Column(String(255), nullable=True)
    range = Column(String(255), nullable=True)
    output = Column(String(255), nullable=True)
    voltage = Column(String(255), nullable=True)
    connection = Column(String(255), nullable=True)
    material = Column(String(255), nullable=True)
    images = Column(String(255), nullable=True)
    pdf = Column(String(255), nullable=True)

# Create tables (only needed once)
Base.metadata.create_all(bind=engine)

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Models for Request/Response
class ProductBase(BaseModel):
    code: Optional[str]
    main_cat: Optional[str]
    sub_cat: Optional[str]
    brand: Optional[str]
    model: Optional[str]
    housing_size: Optional[str]
    function: Optional[str]
    range: Optional[str]
    output: Optional[str]
    voltage: Optional[str]
    connection: Optional[str]
    material: Optional[str]
    images: Optional[str]
    pdf: Optional[str]

class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode = True

class ProductUpdate(ProductBase):
    pass

# API Endpoints
@app.get("/products", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/products/code/{code}", response_model=List[ProductResponse])
def get_products_by_code(code: str, db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.code == code).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found with this code")
    return products

@app.delete("/products/{product_id}")
def delete_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"detail": "Product deleted successfully"}

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product_by_id(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product_update.dict(exclude_unset=True).items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product
