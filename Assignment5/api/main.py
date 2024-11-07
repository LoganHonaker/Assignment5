from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .models import models, schemas
from .controllers import orders, sandwiches, resources, recipes, order_details  # Import controllers
from .dependencies.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Example routes for 'orders' controller
@app.post("/orders/", response_model=schemas.Order, tags=["Orders"])
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return orders.create(db=db, order=order)

@app.get("/orders/", response_model=list[schemas.Order], tags=["Orders"])
def read_orders(db: Session = Depends(get_db)):
    return orders.read_all(db)

# Repeat similar routes for 'sandwiches', 'resources', 'recipes', 'order_details'
