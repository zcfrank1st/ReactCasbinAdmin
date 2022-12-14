from typing import List, Union

import databases
import sqlalchemy
from sqlalchemy import desc, func, select
from fastapi import FastAPI, Response, Depends
from entity import Policy, PolicyIn, User, UserIn, Role, RoleIn, UserRoleRelation, UserRoleRelationIn
import json
import ast

from pydantic import BaseSettings

class Settings(BaseSettings):
    is_dev = True
    database_url = 'postgresql+psycopg2://postgres:1234@127.0.0.1/postgres'

settings = Settings()

database = databases.Database(settings.database_url)
metadata = sqlalchemy.MetaData()
policies = sqlalchemy.Table(
    "casbin_rule",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("ptype", sqlalchemy.String),
    sqlalchemy.Column("v0", sqlalchemy.String),
    sqlalchemy.Column("v1", sqlalchemy.String),
    sqlalchemy.Column("v2", sqlalchemy.String),
    sqlalchemy.Column("v3", sqlalchemy.String),
    sqlalchemy.Column("v4", sqlalchemy.String),
    sqlalchemy.Column("v5", sqlalchemy.String),
)
users = sqlalchemy.Table(
    "user",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_name", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String),
)
roles = sqlalchemy.Table(
    "role",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("role_name", sqlalchemy.String),
)
user_role_relations = sqlalchemy.Table(
    "user_role_relation",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer),
    sqlalchemy.Column("role_id", sqlalchemy.Integer),
)
engine = sqlalchemy.create_engine(settings.database_url)
metadata.create_all(engine)

app = FastAPI()

if settings.is_dev:
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"]
    )
else:
    from fastapi.staticfiles import StaticFiles
    app.mount("/static", StaticFiles(directory="static", html=True), name='static')


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# Policies API
# =====================
@app.get("/policies/", response_model=List[Policy])
async def get_list_policies(response: Response, filter, sort = '[]', range = '[]'):
    sort = ast.literal_eval(sort)
    range = ast.literal_eval(range)
    filter = json.loads(filter)

    if not range and not sort:
        query = policies.select().where(policies.c.id.in_(filter['id'])).order_by(policies.c.id.asc())
        return await database.fetch_all(query)

    count_query = select([func.count()]).select_from(policies)
    count = await database.execute(count_query)
    
    response.headers["Content-Range"] = "policies {0}-{1}/{2}".format(range[0], range[1], count)

    if not filter:
        if sort[1] == 'DESC':
            query = policies.select().order_by(desc(sort[0])).offset(range[0]).fetch(range[1]-range[0]+1)
        else:
            query = policies.select().order_by(sort[0]).offset(range[0]).fetch(range[1]-range[0]+1)
    else:
        if sort[1] == 'DESC':
            query = policies.select().filter_by(**filter).order_by(desc(sort[0])).offset(range[0]).fetch(range[1]-range[0]+1)
        else:
            query = policies.select().filter_by(**filter).order_by(sort[0]).offset(range[0]).fetch(range[1]-range[0]+1)
    return await database.fetch_all(query)


@app.get("/policies/{policy_id}", response_model=Policy)
async def get_one_policy(policy_id:int):
    query = policies.select().where(policies.c.id == policy_id)
    return await database.fetch_one(query)

@app.post("/policies/")
async def create_one_policy(policy_in: PolicyIn):
    create = policies.insert().values(\
        ptype=policy_in.ptype, \
        v0=policy_in.v0, \
        v1=policy_in.v1, \
        v2=policy_in.v2, \
        v3=policy_in.v3, \
        v4=policy_in.v4, \
        v5=policy_in.v5, \
    )
    last_record_id = await database.execute(create)
    return {**policy_in.dict(), "id": last_record_id}

@app.put("/policies/{policy_id}")
async def update_one_policy(policy_id: int, policy_in: PolicyIn):
    update = policies.update().where(policies.c.id == policy_id).values(**policy_in.dict())
    await database.execute(update)
    query = policies.select().where(policies.c.id == policy_id)
    return await database.fetch_one(query)

# @app.put("/policies/")
# async def update_many_policies(filter, policy_in: PolicyIn):
#     filter_request = json.loads(filter)
#     update = policies.update().where(policies.c.id.in_(filter_request['ids'])).values(**policy_in.dict())
#     await database.execute(update)
#     return filter_request['ids']

@app.delete("/policies/{policy_id}")
async def delete_one_policy(policy_id: int):
    query = policies.select().where(policies.c.id == policy_id)
    target = await database.fetch_one(query)
    delete = policies.delete().where(policies.c.id == policy_id)
    await database.execute(delete)
    return target

@app.delete("/policies/")
async def delete_many_policies(filter):
    filter_request = json.loads(filter)
    delete = policies.delete().where(policies.c.id.in_(filter_request['ids']))
    await database.execute(delete)
    return filter_request['ids']

# Users API
# =====================
@app.get("/users/", response_model=List[User])
async def get_list_users(response: Response, filter, sort = '[]', range = '[]'):
    sort = ast.literal_eval(sort)
    range = ast.literal_eval(range)
    filter = json.loads(filter)

    if not range and not sort:
        query = users.select().where(users.c.id.in_(filter['id'])).order_by(users.c.id.asc())
        return await database.fetch_all(query)

    count_query = select([func.count()]).select_from(users)
    count = await database.execute(count_query)
    
    response.headers["Content-Range"] = "users {0}-{1}/{2}".format(range[0], range[1], count)

    print(sort)

    if not filter:
        if sort[1] == 'DESC':
            print('desc')
            query = users.select().order_by(desc(sort[0])).offset(range[0]).fetch(range[1]-range[0]+1)
        else:
            print('asc')
            query = users.select().order_by(sort[0]).offset(range[0]).fetch(range[1]-range[0]+1)
    else:
        if sort[1] == 'DESC':
            query = users.select().filter_by(**filter).order_by(desc(sort[0])).offset(range[0]).fetch(range[1]-range[0]+1)
        else:
            query = users.select().filter_by(**filter).order_by(sort[0]).offset(range[0]).fetch(range[1]-range[0]+1)
    return await database.fetch_all(query)


@app.get("/users/{user_id}", response_model=User)
async def get_one_user(user_id:int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)

@app.post("/users/")
async def create_one_user(user_in: UserIn):
    create = users.insert().values(\
        user_name=user_in.user_name, \
        password=user_in.password, 
    )
    last_record_id = await database.execute(create)
    return {**user_in.dict(), "id": last_record_id}

@app.put("/users/{user_id}")
async def update_one_user(user_id: int, user_in: UserIn):
    update = users.update().where(users.c.id == user_id).values(**user_in.dict())
    await database.execute(update)
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)

# @app.put("/users/")
# async def update_many_users(filter, user_in: UserIn):
#     filter_request = json.loads(filter)
#     update = users.update().where(users.c.id.in_(filter_request['ids'])).values(**user_in.dict())
#     await database.execute(update)
#     return filter_request['ids']

@app.delete("/users/{user_id}")
async def delete_one_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    target = await database.fetch_one(query)
    delete = users.delete().where(users.c.id == user_id)
    await database.execute(delete)
    return target

@app.delete("/users/")
async def delete_many_users(filter):
    filter_request = json.loads(filter)
    delete = users.delete().where(users.c.id.in_(filter_request['ids']))
    await database.execute(delete)
    return filter_request['ids']


# Roles API
# =====================
@app.get("/roles/", response_model=List[Role])
async def get_list_roles(response: Response, filter, sort = '[]', range = '[]'):
    sort = ast.literal_eval(sort)
    range = ast.literal_eval(range)
    filter = json.loads(filter)

    if not range and not sort:
        query = roles.select().where(roles.c.id.in_(filter['id'])).order_by(roles.c.id.asc())
        return await database.fetch_all(query)

    count_query = select([func.count()]).select_from(roles)
    count = await database.execute(count_query)
    
    response.headers["Content-Range"] = "roles {0}-{1}/{2}".format(range[0], range[1], count)

    if not filter:
        if sort[1] == 'DESC':
            query = roles.select().order_by(desc(sort[0])).offset(range[0]).fetch(range[1]-range[0]+1)
        else:
            query = roles.select().order_by(sort[0]).offset(range[0]).fetch(range[1]-range[0]+1)
    else:
        if sort[1] == 'DESC':
            query = roles.select().filter_by(**filter).order_by(desc(sort[0])).offset(range[0]).fetch(range[1]-range[0]+1)
        else:
            query = roles.select().filter_by(**filter).order_by(sort[0]).offset(range[0]).fetch(range[1]-range[0]+1)
    return await database.fetch_all(query)


@app.get("/roles/{role_id}", response_model=Role)
async def get_one_role(role_id:int):
    query = roles.select().where(roles.c.id == role_id)
    return await database.fetch_one(query)

@app.post("/roles/")
async def create_one_role(role_in: RoleIn):
    create = roles.insert().values(\
        role_name=role_in.role_name, 
    )
    last_record_id = await database.execute(create)
    return {**role_in.dict(), "id": last_record_id}

@app.put("/roles/{role_id}")
async def update_one_role(role_id: int, role_in: RoleIn):
    update = roles.update().where(roles.c.id == role_id).values(**role_in.dict())
    await database.execute(update)
    query = roles.select().where(roles.c.id == role_id)
    return await database.fetch_one(query)

# @app.put("/roles/")
# async def update_many_roles(filter, role_in: RoleIn):
#     filter_request = json.loads(filter)
#     update = roles.update().where(roles.c.id.in_(filter_request['ids'])).values(**role_in.dict())
#     await database.execute(update)
#     return filter_request['ids']

@app.delete("/roles/{role_id}")
async def delete_one_role(role_id: int):
    query = roles.select().where(roles.c.id == role_id)
    target = await database.fetch_one(query)
    delete = roles.delete().where(roles.c.id == role_id)
    await database.execute(delete)
    return target

@app.delete("/roles/")
async def delete_many_roles(filter):
    filter_request = json.loads(filter)
    delete = roles.delete().where(roles.c.id.in_(filter_request['ids']))
    await database.execute(delete)
    return filter_request['ids']

# UserRoleRelations API
# =====================
@app.get("/user_role_relations/", response_model=List[UserRoleRelation])
async def get_list_relations(sort, range, filter, response: Response):
    sort = ast.literal_eval(sort)
    range = ast.literal_eval(range)
    filter = json.loads(filter)

    count_query = select([func.count()]).select_from(user_role_relations)
    count = await database.execute(count_query)
    
    response.headers["Content-Range"] = "user_role_relations {0}-{1}/{2}".format(range[0], range[1], count)

    if not filter:
        if sort[1] == 'DESC':
            query = user_role_relations.select().order_by(desc(sort[0])).offset(range[0]).fetch(range[1]-range[0]+1)
        else:
            query = user_role_relations.select().order_by(sort[0]).offset(range[0]).fetch(range[1]-range[0]+1)
    else:
        if sort[1] == 'DESC':
            query = user_role_relations.select().filter_by(**filter).order_by(desc(sort[0])).offset(range[0]).fetch(range[1]-range[0]+1)
        else:
            query = user_role_relations.select().filter_by(**filter).order_by(sort[0]).offset(range[0]).fetch(range[1]-range[0]+1)
    return await database.fetch_all(query)


@app.get("/user_role_relations/{relation_id}", response_model=UserRoleRelation)
async def get_one_relation(relation_id:int):
    query = user_role_relations.select().where(user_role_relations.c.id == relation_id)
    return await database.fetch_one(query)

@app.post("/user_role_relations/")
async def create_one_relation(relation_in: UserRoleRelationIn):
    create = user_role_relations.insert().values(\
        user_id = relation_in.user_id, \
        role_id = relation_in.role_id,
    )
    last_record_id = await database.execute(create)
    return {**relation_in.dict(), "id": last_record_id}

@app.put("/user_role_relations/{relation_id}")
async def update_one_relation(relation_id: int, relation_in: UserRoleRelationIn):
    update = user_role_relations.update().where(user_role_relations.c.id == relation_id).values(**relation_in.dict())
    await database.execute(update)
    query = user_role_relations.select().where(user_role_relations.c.id == relation_id)
    return await database.fetch_one(query)

# @app.put("/user_role_relations/")
# async def update_many_relations(filter, relation_in: UserRoleRelationIn):
#     filter_request = json.loads(filter)
#     update = user_role_relations.update().where(user_role_relations.c.id.in_(filter_request['ids'])).values(**relation_in.dict())
#     await database.execute(update)
#     return filter_request['ids']

@app.delete("/user_role_relations/{relation_id}")
async def delete_one_relation(relation_id: int):
    query = user_role_relations.select().where(user_role_relations.c.id == relation_id)
    target = await database.fetch_one(query)
    delete = user_role_relations.delete().where(user_role_relations.c.id == relation_id)
    await database.execute(delete)
    return target

@app.delete("/user_role_relations/")
async def delete_many_roles(filter):
    filter_request = json.loads(filter)
    delete = user_role_relations.delete().where(user_role_relations.c.id.in_(filter_request['ids']))
    await database.execute(delete)
    return filter_request['ids']