<p align="center">
  <a href="https://mithun2003.github.io/CRUDFastAPI/">
    <!-- <img src="https://github.com/mithun2003/CRUDFastAPI/blob/main/assets/CRUDFastAPI.png?raw=true" alt="CRUDFastAPI written in white with a drawing of a gear and inside this gear a bolt." width="45%" height="auto"> -->
  </a>
</p>
<p align="center" markdown=1>
  <i>Powerful CRUD methods and automatic endpoint creation for FastAPI.</i>
</p>
<p align="center" markdown=1>
<a href="https://github.com/mithun2003/CRUDFastAPI/actions/workflows/tests.yml">
  <img src="https://github.com/mithun2003/CRUDFastAPI/actions/workflows/tests.yml/badge.svg" alt="Tests"/>
</a>
<a href="https://pypi.org/project/CRUDFastAPI/">
  <img src="https://img.shields.io/pypi/v/CRUDFastAPI?color=%2334D058&label=pypi%20package" alt="PyPi Version"/>
</a>
<a href="https://pypi.org/project/CRUDFastAPI/">
  <img src="https://img.shields.io/pypi/pyversions/CRUDFastAPI.svg?color=%2334D058" alt="Supported Python Versions"/>
</a>
<a href="https://codecov.io/gh/mithun2003/CRUDFastAPI" > 
  <img src="https://codecov.io/gh/mithun2003/CRUDFastAPI/graph/badge.svg?token=J7XUP29RKU"/> 
</a>
</p>
<hr>
<p align="justify">
<b>CRUDFastAPI</b> is a Python package for <b>FastAPI</b>, offering robust async CRUD operations and flexible endpoint creation utilities, streamlined through advanced features like <b>auto-detected join</b> conditions, <b>dynamic sorting</b>, and offset and cursor <b>pagination</b>.
</p>
<hr>
<h2>Features</h2>

- ⚡️ **Fully Async**: Leverages Python's async capabilities for non-blocking database operations.
- 📚 **SQLAlchemy 2.0**: Works with the latest SQLAlchemy version for robust database interactions.
- 🦾 **Powerful CRUD Functionality**: Full suite of efficient CRUD operations with support for joins.
- ⚙️ **Dynamic Query Building**: Supports building complex queries dynamically, including filtering, sorting, and pagination.
- 🤝 **Advanced Join Operations**: Facilitates performing SQL joins with other models with automatic join condition detection.
- 📖 **Built-in Offset Pagination**: Comes with ready-to-use offset pagination.
- ➤ **Cursor-based Pagination**: Implements efficient pagination for large datasets, ideal for infinite scrolling interfaces.
- 🤸‍♂️ **Modular and Extensible**: Designed for easy extension and customization to fit your requirements.
- 🛣️ **Auto-generated Endpoints**: Streamlines the process of adding CRUD endpoints with custom dependencies and configurations.

<h2>Requirements</h2>
<p>Before installing CRUDFastAPI, ensure you have the following prerequisites:</p>
<ul>
  <li><b>Python:</b> Version 3.9 or newer.</li>
  <li><b>FastAPI:</b> CRUDFastAPI is built to work with FastAPI, so having FastAPI in your project is essential.</li>
  <li><b>SQLAlchemy:</b> Version 2.0.21 or newer. CRUDFastAPI uses SQLAlchemy for database operations.</li>
  <li><b>Pydantic:</b> Version 2.4.1 or newer. CRUDFastAPI leverages Pydantic models for data validation and serialization.</li>
  <li><b>SQLAlchemy-Utils:</b> Optional, but recommended for additional SQLAlchemy utilities.</li>
</ul>

<h2>Installing</h2>

To install, just run:

```sh
pip install CRUDFastAPI
```

Or, if using poetry:

```sh
poetry add CRUDFastAPI
```

<h2>Usage</h2>

CRUDFastAPI offers two primary ways to use its functionalities:

1. By using `crud_router` for automatic endpoint creation.
2. By integrating `CRUDFastAPI` directly into your FastAPI endpoints for more control.

Below are examples demonstrating both approaches:

<h3>Using crud_router for Automatic Endpoint Creation</h3>

Here's a quick example to get you started:

<h4>Define Your Model and Schema</h4>

**models.py**

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
```

**schemas.py**

```python
from pydantic import BaseModel

class ItemCreateSchema(BaseModel):
    name: str
    description: str

class ItemUpdateSchema(BaseModel):
    name: str
    description: str
```

<h4>Set Up FastAPI and CRUDFastAPI</h4>

**main.py**

```python
from typing import AsyncGenerator

from fastapi import FastAPI
from CRUDFastAPI import CRUDFastAPI, crud_router
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from yourapp.models import Base, Item
from yourapp.schemas import ItemCreateSchema, ItemUpdateSchema

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

# CRUD router setup
item_router = crud_router(
    session=get_session,
    model=Item,
    create_schema=ItemCreateSchema,
    update_schema=ItemUpdateSchema,
    path="/items",
    tags=["Items"],
)

app.include_router(item_router)

```

<h3>Using CRUDFastAPI in User-Defined FastAPI Endpoints</h3>

For more control over your endpoints, you can use CRUDFastAPI directly within your custom FastAPI route functions. Here's an example:

**main.py**

```python
from typing import AsyncGenerator

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from CRUDFastAPI import CRUDFastAPI

from models import Base, Item
from schemas import ItemCreateSchema, ItemUpdateSchema

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

# Instantiate CRUDFastAPI with your model
item_crud = CRUDFastAPI(Item)

@app.post("/custom/items/")
async def create_item(
    item_data: ItemCreateSchema, db: AsyncSession = Depends(get_session)
):
    return await item_crud.create(db, item_data)

@app.get("/custom/items/{item_id}")
async def read_item(item_id: int, db: AsyncSession = Depends(get_session)):
    item = await item_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# You can add more routes for update and delete operations in a similar fashion
```

In this example, we define custom endpoints for creating and reading items using CRUDFastAPI directly, providing more flexibility in how the endpoints are structured and how the responses are handled.


## References

- This project was heavily inspired by CRUDBase in [`FastAPI Microservices`](https://github.com/Kludex/fastapi-microservices) by [@kludex](https://github.com/kludex).
- Thanks [@ada0l](https://github.com/ada0l) for the PyPI package name!

## Similar Projects

- **[flask-muck](https://github.com/dtiesling/flask-muck)** - _"I'd love something like this for flask"_ There you have it
- **[FastAPI CRUD Router](https://github.com/awtkns/fastapi-crudrouter)** - Supports multiple ORMs, but currently unmantained
- **[FastAPI Quick CRUD](https://github.com/LuisLuii/FastAPIQuickCRUD)** - Same purpose, but only for SQLAlchemy 1.4

## License

[`MIT`](LICENSE.md)

## Contact

[github.com/mithun2003](https://github.com/mithun2003/)
