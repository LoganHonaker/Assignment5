from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import models, schemas

# Create a new resource entry
def create(db: Session, resource: schemas.ResourceCreate):
    db_resource = models.Resource(
        name=resource.name,
        description=resource.description
    )
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

# Retrieve all resources
def read_all(db: Session):
    return db.query(models.Resource).all()

# Retrieve a specific resource by ID
def read_one(db: Session, resource_id: int):
    return db.query(models.Resource).filter(models.Resource.id == resource_id).first()

# Update a resource entry
def update(db: Session, resource_id: int, resource: schemas.ResourceUpdate):
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id)
    if not db_resource.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    update_data = resource.dict(exclude_unset=True)
    db_resource.update(update_data, synchronize_session=False)
    db.commit()
    return db_resource.first()

# Delete a resource entry
def delete(db: Session, resource_id: int):
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id)
    if not db_resource.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    db_resource.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
