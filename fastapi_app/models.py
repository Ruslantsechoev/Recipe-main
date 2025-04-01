from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

recipe_category = Table(
    'recipe_category', Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)

class Recipe(Base):
    __tablename__ = "recipes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True)
    description = Column(Text)
    steps = Column(Text)
    cooking_time = Column(Integer)
    image = Column(String(255), nullable=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    
    categories = relationship("Category", secondary=recipe_category, back_populates="recipes")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True)
    description = Column(Text)
    
    recipes = relationship("Recipe", secondary=recipe_category, back_populates="categories")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True)
    email = Column(String(255))