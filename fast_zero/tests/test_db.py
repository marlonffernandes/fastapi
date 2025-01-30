from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):

    user = User(username="test1", password="test", email="test1@test.com")
    session.add(user)
    session.commit()
    result = session.scalar(select(User).where(User.email == "test1@test.com"))
    session.refresh(user)

    assert user.id == 1
    assert result.id == 1
