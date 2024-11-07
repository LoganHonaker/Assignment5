from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import models, schemas

# Create a new recipe entry
def create(db: Session, recipe: schemas.RecipeCreate):
    db_recipe = models.Recipe(
        name=recipe.name,
        ingredients=recipe.ingredients,
        instructions=recipe.instructions
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

# Retrieve all recipes
def read_all(db: Session):
    return db.query(models.Recipe).all()

# Retrieve a specific recipe by ID
def read_one(db: Session, recipe_id: int):
    return db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()

# Update a recipe entry
def update(db: Session, recipe_id: int, recipe: schemas.RecipeUpdate):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id)
    if not db_recipe.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    update_data = recipe.dict(exclude_unset=True)
    db_recipe.update(update_data, synchronize_session=False)
    db.commit()
    return db_recipe.first()

# Delete a recipe entry
def delete(db: Session, recipe_id: int):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id)
    if not db_recipe.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    db_recipe.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
