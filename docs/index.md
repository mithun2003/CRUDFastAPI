<style>
    .md-typeset h1,
    .md-content__button {
        display: none;
    }
</style>

<p align="center">
  <a href="https://github.com/mithunthomas2003/CRUDFastAPI">
    <img src="assets/CRUDFastAPI.png?raw=true" alt="CRUDFastAPI written in white with a drawing of a gear and inside this gear a bolt." width="45%" height="auto">
  </a>
</p>
<p align="center" markdown=1>
  <i>Powerful CRUD methods and automatic endpoint creation for FastAPI.</i>
</p>
<p align="center" markdown=1>
<a href="https://github.com/mithunthomas2003/CRUDFastAPI/actions/workflows/tests.yml">
  <img src="https://github.com/mithunthomas2003/CRUDFastAPI/actions/workflows/tests.yml/badge.svg" alt="Tests"/>
</a>
<a href="https://pypi.org/project/CRUDFastAPI/">
  <img src="https://img.shields.io/pypi/v/CRUDFastAPI?color=%2334D058&label=pypi%20package" alt="PyPi Version"/>
</a>
<a href="https://pypi.org/project/CRUDFastAPI/">
  <img src="https://img.shields.io/pypi/pyversions/CRUDFastAPI.svg?color=%2334D058" alt="Supported Python Versions"/>
</a>
</a>
<a href="https://codecov.io/gh/mithunthomas2003/CRUDFastAPI" > 
  <img src="https://codecov.io/gh/mithunthomas2003/CRUDFastAPI/graph/badge.svg?token=J7XUP29RKU"/> 
</a>
</p>
<hr>
<p align="justify">
<b>CRUDFastAPI</b> is a Python package for <b>FastAPI</b>, offering robust async CRUD operations and flexible endpoint creation utilities, streamlined through advanced features like <b>auto-detected join</b> conditions, <b>dynamic sorting</b>, and offset and cursor <b>pagination</b>.
</p>
<hr>

## Features

- **Fully Async**: Leverages Python's async capabilities for non-blocking database operations.
- **SQLAlchemy 2.0**: Works with the latest SQLAlchemy version for robust database interactions.
- **SQLModel Support**: You can optionally use SQLModel 0.14 or newer instead of SQLAlchemy.
- **Powerful CRUD Functionality**: Full suite of efficient CRUD operations with support for joins.
- **Dynamic Query Building**: Supports building complex queries dynamically, including filtering, sorting, and pagination.
- **Advanced Join Operations**: Facilitates performing SQL joins with other models with automatic join condition detection.
- **Built-in Offset Pagination**: Comes with ready-to-use offset pagination.
- **Cursor-based Pagination**: Implements efficient pagination for large datasets, ideal for infinite scrolling interfaces.
- **Modular and Extensible**: Designed for easy extension and customization to fit your requirements.
- **Auto-generated Endpoints**: Streamlines the process of adding CRUD endpoints with custom dependencies and configurations.

## Minimal Example

Assuming you have your model, schemas and database connection:

```python
# imports here

# define your model
class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)

# your schemas
class ItemSchema(BaseModel):
    name: str

# database connection
DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
```

Use `crud_router` and include it in your `FastAPI` application

```python
from CRUDFastAPI import crud_router

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

# FastAPI app
app = FastAPI(lifespan=lifespan)

item_router = crud_router(
    session=get_session,
    model=Item,
    create_schema=ItemSchema,
    update_schema=ItemSchema,
    path="/items",
    tags=["Items"]
)

app.include_router(item_router)
```

And it's all done, just go to `/docs` and the crud endpoints are created.

## Requirements

<p>Before installing CRUDFastAPI, ensure you have the following prerequisites:</p>
<ul>
  <li><b>Python:</b> Version 3.9 or newer.</li>
  <li><b>FastAPI:</b> CRUDFastAPI is built to work with FastAPI, so having FastAPI in your project is essential.</li>
  <li><b>SQLAlchemy or SQLModel:</b> CRUDFastAPI uses SQLAlchemy 2.0 for database operations, so you need SQLAlchemy 2.0 or newer or SQLModel 0.14 or newer.</li>
  <li><b>Pydantic V2 or SQLModel:</b> CRUDFastAPI leverages Pydantic models for data validation and serialization, so you need Pydantic 2.0 or newer or SQLModel 0.14 or newer.</li>
</ul>

## Installing

To install, just run:

```sh
pip install CRUDFastAPI
```

Or, if using poetry:

```sh
poetry add CRUDFastAPI
```

## Usage

CRUDFastAPI offers two primary ways to use its functionalities:

1. By using `crud_router` for automatic endpoint creation.
2. By integrating `CRUDFastAPI` directly into your FastAPI endpoints for more control.

Below are examples demonstrating both approaches:

### Using crud_router for Automatic Endpoint Creation

Here's a quick example to get you started:

#### Define Your Model and Schema

```python title="models/item.py"
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel

class Base(DeclarativeBase):
    pass

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

class ItemCreateSchema(BaseModel):
    name: str
    description: str

class ItemUpdateSchema(BaseModel):
    name: str
    description: str

```

#### Set Up FastAPI and CRUDFastAPI

```python title="main.py"
from typing import AsyncGenerator

from fastapi import FastAPI
from CRUDFastAPI import crud_router
from CRUDFastAPI import CRUDFastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from item import Base, Item, ItemCreateSchema, ItemUpdateSchema

# Database setup (Async SQLAlchemy)
DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Database session dependency
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

# Create tables before the app start
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

# FastAPI app
app = FastAPI(lifespan=lifespan)

# CRUD operations setup
crud = CRUDFastAPI(Item)

# CRUD router setup
item_router = crud_router(
    session=get_session,
    model=Item,
    create_schema=ItemCreateSchema,
    update_schema=ItemUpdateSchema,
    path="/items",
    tags=["Items"]
)

app.include_router(item_router)
```

### Using CRUDFastAPI in User-Defined FastAPI Endpoints

For more control over your endpoints, you can use CRUDFastAPI directly within your custom FastAPI route functions. Here's an example:

```python title="api/v1/item.py" hl_lines="10 14 18"
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from CRUDFastAPI import CRUDFastAPI
from yourapp.models import Item
from yourapp.schemas import ItemCreateSchema, ItemUpdateSchema

# Assume async_session is already set up as per the previous example

# Instantiate CRUDFastAPI with your model
item_crud = CRUDFastAPI(Item)

@app.post("/custom/items/")
async def create_item(item_data: ItemCreateSchema, db: AsyncSession = Depends(get_session)):
    return await item_crud.create(db, item_data)

@app.get("/custom/items/{item_id}")
async def read_item(item_id: int, db: AsyncSession = Depends(get_session)):
    item = await item_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# You can add more routes for update and delete operations in a similar fashion
```

## License

[`MIT`](community/LICENSE.md)
