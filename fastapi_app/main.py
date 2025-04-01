from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Recipe, Category
from schemas import RecipeBase, RecipeResponse, RecipeUpdate, CategoryBase
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/recipes/", response_model=list[RecipeResponse])
def get_all_recipes(db: Session = Depends(get_db)):
    return db.query(models.Recipe).all()

@app.get("/recipes/{recipe_id}", response_model=RecipeResponse)
def get_recipe_by_id(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@app.get("/recipes/search/{title}", response_model=list[RecipeResponse])
def search_by_title(title: str, db: Session = Depends(get_db)):
    return db.query(models.Recipe).filter(models.Recipe.title.ilike(f"%{title}%")).all()

@app.get("/recipes/category/{category_name}", response_model=list[RecipeResponse])
def get_by_category(category_name: str, db: Session = Depends(get_db)):
    return db.query(models.Recipe).join(models.Recipe.categories).filter(
        models.Category.name == category_name
    ).all()

@app.post("/recipes/", response_model=RecipeResponse)
def create_recipe(recipe: RecipeBase, db: Session = Depends(get_db)):
    db_recipe = Recipe(**recipe.dict())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@app.post("/categories/", response_model=CategoryBase)
def create_category(category: CategoryBase, db: Session = Depends(get_db)):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.put("/recipes/{recipe_id}", response_model=RecipeResponse)
def update_recipe(recipe_id: int, recipe: RecipeUpdate, db: Session = Depends(get_db)):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    for key, value in recipe.dict().items():
        if value is not None:
            setattr(db_recipe, key, value)
    
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@app.put("/recipes/{recipe_id}/add_category")
def add_category_to_recipe(recipe_id: int, category: CategoryBase, db: Session = Depends(get_db)):
    db_recipe = db.query(models.Recipe).get(recipe_id)
    db_category = db.query(models.Category).filter(models.Category.name == category.name).first()
    
    if not db_recipe or not db_category:
        raise HTTPException(status_code=404, detail="Recipe or Category not found")
    
    db_recipe.categories.append(db_category)
    db.commit()
    return {"message": "Category added successfully"}