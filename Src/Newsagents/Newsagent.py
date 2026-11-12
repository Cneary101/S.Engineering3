from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import engine
from models import Newsagent


def verify_name(name):
    return isinstance(name, str) and name.strip() != ""


# Create
def create_newsagent(newsagent_id, name):
    if type(newsagent_id) is not int or newsagent_id <= 0:
        return False
    if not verify_name(name):
        return False

    with Session(engine) as session:
        if session.get(Newsagent, newsagent_id) is not None:
            return False
        session.add(Newsagent(id=newsagent_id, name=name.strip(), is_active=True))
        try:
            session.commit()
            return newsagent_id
        except IntegrityError:
            session.rollback()
            return False


# Read
def read_newsagent(newsagent_id):
    with Session(engine) as session:
        return session.get(Newsagent, newsagent_id)


def read_all_newsagents():
    with Session(engine) as session:
        return list(session.scalars(select(Newsagent).order_by(Newsagent.id)))


# Update
def update_newsagent(newsagent_id, name):
    if not verify_name(name):
        return False
    with Session(engine) as session:
        newsagent = session.get(Newsagent, newsagent_id)
        if newsagent is None:
            return False
        newsagent.name = name.strip()
        session.commit()
        return True


# Delete: deactivate to keep historical records
def delete_newsagent(newsagent_id):
    with Session(engine) as session:
        newsagent = session.get(Newsagent, newsagent_id)
        if newsagent is None or not newsagent.is_active:
            return False
        newsagent.is_active = False
        session.commit()
        return True
