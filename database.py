from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import json

db_url = ''

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

server_local = params['local_server']

if server_local == 'True':
    db_url = params['local_uri']
else:
    db_url = params['prod_uri']

engine = create_engine(db_url)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from auth import models
    from post import models
    Base.metadata.create_all(bind=engine)
    print("database migrated successfully....")