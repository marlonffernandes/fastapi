from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.models import User, table_registry


def test_create_user():
    engine = create_engine("sqlite:///:memory:")
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        user = User(username="test1", password="test", email="test1@test.com")
        session.add(user)
        session.commit()
        session.refresh(user)

    assert user.id == 1
