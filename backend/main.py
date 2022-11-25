from typing import List

import databases
import sqlalchemy
from sqlalchemy import desc, func, select
from fastapi import FastAPI, Response
from entity import Policy, PolicyIn
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

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# API
@app.get("/policies/", response_model=List[Policy])
async def get_list_policies(sort, range, filter, response: Response):
    sort = ast.literal_eval(sort)
    range = ast.literal_eval(range)
    filter = json.loads(filter)

    count_query = select([func.count()]).select_from(policies)
    count = await database.execute(count_query)
    print(count)
    response.headers["Content-Range"] = "policies {0}-{1}/{2}".format(range[0], range[1], count)

    if not filter:
        if sort[0] == 'DESC':
            query = policies.select().order_by(desc(sort[0])).offset(range[0]).fetch(range[1]-range[0]+1)
        else:
            query = policies.select().order_by(sort[0]).offset(range[0]).fetch(range[1]-range[0]+1)
    else:
        if sort[0] == 'DESC':
            query = policies.select().filter_by(**filter).order_by(desc(sort[0])).offset(range[0]).fetch(range[1]-range[0]+1)
        else:
            query = policies.select().filter_by(**filter).order_by(sort[0]).offset(range[0]).fetch(range[1]-range[0]+1)
    return await database.fetch_all(query)


@app.get("/policies/{policy_id}", response_model=Policy)
async def get_one_policy(policy_id:int):
    query = policies.select().where(policies.c.id == policy_id)
    return await database.fetch_one(query)

@app.get("/policies/", response_model=List[Policy])
async def get_many_policies(filter):
    filter_request = json.loads(filter)
    query = policies.select().where(policies.c.id.in_(filter_request['ids'])).order_by(policies.c.id.asc())
    return await database.fetch_all(query)

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

@app.put("/policies/")
async def update_many_policies(filter, policy_in: PolicyIn):
    filter_request = json.loads(filter)
    update = policies.update().where(policies.c.id.in_(filter_request['ids'])).values(**policy_in.dict())
    await database.execute(update)
    return filter_request['ids']

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