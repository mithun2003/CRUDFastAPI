
# Comprehensive Guide to Joins in CRUDFastAPI

CRUDFastAPI simplifies CRUD operations while offering capabilities for handling complex data relationships. This guide thoroughly explores the use of `JoinConfig` for executing join operations in CRUDFastAPI methods such as `count`, `get_joined`, and `get_multi_joined`, alongside simplified join techniques for straightforward scenarios.

## Understanding `JoinConfig`

`JoinConfig` is a detailed configuration mechanism for specifying joins between models in CRUDFastAPI queries. It contains the following key attributes:

- **`model`**: The SQLAlchemy model to join.
- **`join_on`**: The condition defining how the join connects to other models.
- **`join_prefix`**: An optional prefix for the joined columns to avoid column name conflicts.
- **`schema_to_select`**: An optional Pydantic schema for selecting specific columns from the joined model.
- **`join_type`**: The type of join (e.g., "left", "inner").
- **`alias`**: An optional SQLAlchemy `AliasedClass` for complex scenarios like self-referential joins or multiple joins on the same model.
- **`filters`**: An optional dictionary to apply filters directly to the joined model.

## Applying Joins in CRUDFastAPI Methods

### The `count` Method with Joins

The `count` method can be enhanced with join operations to perform complex aggregate queries. While `count` primarily returns the number of records matching a given condition, introducing joins allows for counting records across related models based on specific relationships and conditions.

#### Using `JoinConfig`

For join requirements, the `count` method can be invoked with join parameters passed as a list of `JoinConfig` to the `joins_config` parameter:

```python
from CRUDFastAPI import JoinConfig
# Count the number of tasks assigned to users in a specific department
task_count = await task_crud.count(
    db=db,
    joins_config=[
        JoinConfig(
            model=User, 
            join_on=Task.assigned_user_id == User.id
        ),
        JoinConfig(
            model=Department, 
            join_on=User.department_id == Department.id, 
            filters={"name": "Engineering"}
        )
    ]
)
```

### Fetching Data with `get_joined` and `get_multi_joined`

These methods are essential for retrieving records from a primary model while including related data from one or more joined models. They support both simple and complex joining scenarios, including self-referential joins and many-to-many relationships.

#### Simple Joins Using Base Parameters

For simpler join requirements, CRUDFastAPI allows specifying join parameters directly:

- **`model`**: The target model to join.
- **`join_on`**: The join condition.
- **`join_type`**: Specifies the SQL join type.
- **`join_prefix`**: Optional prefix for columns from the joined model.
- **`alias`**: An optional SQLAlchemy `AliasedClass` for complex scenarios like self-referential joins or multiple joins on the same model.
- **`filters`**: Additional filters for the joined model.

#### Examples of Simple Joining

```python
# Fetch tasks with user details, specifying a left join
tasks_with_users = await task_crud.get_joined(
    db=db,
    join_model=User,
    join_on=Task.user_id == User.id,
    join_type="left"
)
```

#### Getting Joined Data Nested

Note that by default, `CRUDFastAPI` joins all the data and returns it in a single dictionary.
Let's define two tables:
```python
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    tier_id = Column(Integer, ForeignKey("tier.id"))


class Tier(Base):
    __tablename__ = "tier"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
```

And join them with `CRUDFastAPI`:

```python
user_tier = await user_crud.get_joined(
    db=db,
    join_model=Tier,
    join_on=User.tier_id == Tier.id,
    join_type="left",
    join_prefix="tier_",,
    id=1
)
```

We'll get:

```javascript
{
    "id": 1,
    "name": "Example",
    "tier_id": 1,
    "tier_name": "Free",
}
```

If you want the joined data in a nested dictionary instead, you may just pass `nest_joins=True`:

```python
user_tier = await user_crud.get_joined(
    db=db,
    join_model=Tier,
    join_on=User.tier_id == Tier.id,
    join_type="left",
    join_prefix="tier_",
    nest_joins=True,
    id=1,
)
```

And you will get:

```javascript
{
    "id": 1,
    "name": "Example",
    "tier": {
        "id": 1,
        "name": "Free",
    },
}
```

This works for both `get_joined` and `get_multi_joined`.

!!! WARNING
    Note that the final `"_"` in the passed `"tier_"` is stripped.

### Complex Joins Using `JoinConfig`

When dealing with more complex join conditions, such as multiple joins, self-referential joins, or needing to specify aliases and filters, `JoinConfig` instances become the norm. They offer granular control over each join's aspects, enabling precise and efficient data retrieval.

```python
# Fetch users with details from related departments and roles, using aliases for self-referential joins
from CRUDFastAPI import aliased
manager_alias = aliased(User)

users = await user_crud.get_multi_joined(
    db=db,
    schema_to_select=UserSchema,
    joins_config=[
        JoinConfig(
            model=Department, 
            join_on=User.department_id == Department.id, 
            join_prefix="dept_"
        ),
        JoinConfig(
            model=Role, 
            join_on=User.role_id == Role.id, 
            join_prefix="role_"
        ),
        JoinConfig(
            model=User, 
            alias=manager_alias, 
            join_on=User.manager_id == manager_alias.id, 
            join_prefix="manager_"
        )
    ]
)
```

#### Many-to-Many Relationships with `get_multi_joined`

CRUDFastAPI simplifies dealing with many-to-many relationships by allowing easy fetch operations with joined models. Here, we demonstrate using `get_multi_joined` to handle a many-to-many relationship between `Project` and `Participant` models, linked through an association table.

**Note on Handling Many-to-Many Relationships:**

When using `get_multi_joined` for many-to-many relationships, it's essential to maintain a specific order in your `joins_config`: 

1. **First**, specify the main table you're querying from.
2. **Next**, include the association table that links your main table to the other table involved in the many-to-many relationship.
3. **Finally**, specify the other table that is connected via the association table.

This order ensures that the SQL joins are structured correctly to reflect the many-to-many relationship and retrieve the desired data accurately.

!!! TIP

    Note that the first one can be the model defined in `CRUDFastAPI(Model)`.

##### Scenario

Imagine a scenario where projects have multiple participants, and participants can be involved in multiple projects. This many-to-many relationship is facilitated through an association table.

##### Models

Our models include `Project`, `Participant`, and an association model `ProjectsParticipantsAssociation`:

```python
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Association table for the many-to-many relationship
projects_participants_association = Table('projects_participants_association', Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True),
    Column('participant_id', Integer, ForeignKey('participants.id'), primary_key=True)
)

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    # Relationship to Participant through the association table
    participants = relationship("Participant", secondary=projects_participants_association)

class Participant(Base):
    __tablename__ = 'participants'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(String)
    # Relationship to Project through the association table
    projects = relationship("Project", secondary=projects_participants_association)
```

##### Fetching Data with `get_multi_joined`

To fetch projects along with their participants, we utilize `get_multi_joined` with appropriate `JoinConfig` settings:

```python
from CRUDFastAPI import CRUDFastAPI, JoinConfig

# Initialize CRUDFastAPI for the Project model
crud_project = CRUDFastAPI(Project)

# Define join conditions and configuration
joins_config = [
    JoinConfig(
        model=ProjectsParticipantsAssociation,
        join_on=Project.id == ProjectsParticipantsAssociation.project_id,
        join_type="inner",
        join_prefix="pp_"
    ),
    JoinConfig(
        model=Participant,
        join_on=ProjectsParticipantsAssociation.participant_id == Participant.id,
        join_type="inner",
        join_prefix="participant_"
    )
]

# Fetch projects with their participants
projects_with_participants = await crud_project.get_multi_joined(
    db_session, 
    joins_config=joins_config
)

# Now, `projects_with_participants['data']` will contain projects along with their participant information.
```

#### Practical Tips for Advanced Joins

- **Prefixing**: Always use the `join_prefix` attribute to avoid column name collisions, especially in complex joins involving multiple models or self-referential joins.
- **Aliasing**: Utilize the `alias` attribute for disambiguating joins on the same model or for self-referential joins.
- **Filtering Joined Models**: Apply filters directly to joined models using the `filters` attribute in `JoinConfig` to refine the data set returned by the query.
- **Ordering Joins**: In many-to-many relationships or complex join scenarios, carefully sequence your `JoinConfig` entries to ensure logical and efficient SQL join construction.

## Conclusion

CRUDFastAPI's support for join operations enhances the ability to perform complex queries across related models in FastAPI applications. By understanding and utilizing the `JoinConfig` class within the `count`, `get_joined`, and `get_multi_joined` methods, developers can craft powerful data retrieval queries.