from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import EmailStr
from sqlalchemy import update

from app.core.security import get_password_hash, verify_password
from app.models import User
from app.schemas import UserCreate, UserOut
from app.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists
from app.utilities.exceptions.password import PasswordDoesNotMatch


async def create_new_user(db: AsyncSession, user: UserCreate) -> User:
    hash_password = get_password_hash(user.password)
    user.password = hash_password

    new_user = User(**user.model_dump())

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def read_user_by_username(db: AsyncSession, username: str) -> User:
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    if not user:
        raise EntityDoesNotExist(f"User with username `{username}` does not exist!")

    return user


async def read_user_by_email(db: AsyncSession, email: EmailStr) -> User:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user:
        raise EntityDoesNotExist(f"User with email `{email}` does not exist!")

    return user


async def is_username_taken(db: AsyncSession, username: str) -> bool:
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    if user:
        raise EntityAlreadyExists(f"The username `{username}` is already taken!")

    return False


async def is_email_taken(db: AsyncSession, email: EmailStr) -> bool:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user:
        raise EntityAlreadyExists(f"The email `{email}` is already registered!")

    return False


async def authenticate(db: AsyncSession, email: EmailStr, password: str) -> User:
    user = await read_user_by_email(db=db, email=email)

    if not verify_password(password, user.password):
        raise PasswordDoesNotMatch(f"Invalid password!")

    return user
