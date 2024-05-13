If you are using SQLModel, go to [Using SQLModel](sqlmodel.md) instead.

## Minimal Example

Assuming you have your SQLAlchemy model, Pydantic schemas and database connection, just skip to [Using CRUDFastAPI](#using-CRUDFastAPI)

### Basic Setup

Define your SQLAlchemy model

```python title="setup.py" hl_lines="9-12"
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

class Base(DeclarativeBase):
    pass

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class ItemCreateSchema(BaseModel):
    name: str

DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
```

Then your Pydantic schemas

```python title="setup.py" hl_lines="14 15"
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

class Base(DeclarativeBase):
    pass

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class ItemCreateSchema(BaseModel):
    name: str

DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
```

And, finally, your database connection

```python title="setup.py" hl_lines="17-19"
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

class Base(DeclarativeBase):
    pass

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class ItemCreateSchema(BaseModel):
    name: str

DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
```

### Using CRUDFastAPI

Use `crud_router` and include it in your `FastAPI` application

```python title="main.py" hl_lines="17-24 26"
from CRUDFastAPI import crud_router

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

item_router = crud_router(
    session=session,
    model=Item,
    create_schema=ItemSchema,
    update_schema=ItemSchema,
    path="/items",
    tags=["Items"]
)

app.include_router(item_router)
```

And it's all done, just go to `/docs` and the crud endpoints are created.
