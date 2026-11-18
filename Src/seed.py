# src/seed.py


from sqlalchemy.orm import Session
from database import engine
from Login import LoginManager
from models import User, DeliveryArea


def seed_admin(session):
    if session.query(User).first() is not None:
        print("Users already present — skipping admin seed.")
        return
    lm = LoginManager(session)
    ok = lm.create_user("admin1", "1234", "admin")
    print(f"Admin user 'admin1' created: {ok}")


def seed_delivery_areas(session):
    if session.query(DeliveryArea).first() is not None:
        print("Delivery areas already present — skipping area seed.")
        return
    for name in ("North", "South", "East", "West", "Central"):
        session.add(DeliveryArea(name=name))
    session.commit()
    print("Seeded 5 delivery areas.")


def main():
    with Session(engine) as session:
        seed_admin(session)
        seed_delivery_areas(session)


if __name__ == "__main__":
    main()