import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from src.core.database import Base, get_db
from src.core.security import encrypt_password
from src.main import app
from tests.users.factories import UserFactory

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
    )
TestingSessionLocal = async_sessionmaker(engine_test, expire_on_commit=False)

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    app.dependency_overrides[get_db] = override_get_db

    yield

    app.dependency_overrides.clear()

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def db_session():
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:
        yield ac

@pytest_asyncio.fixture
async def user(db_session):
    password = "testtest"
    user = UserFactory(password=encrypt_password(password))

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    user.clean_password = password

    return user

@pytest_asyncio.fixture
async def other_user(db_session):
    password = "12345678"
    user = UserFactory(password=encrypt_password(password))
    
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    user.clean_password = password

    return user

@pytest_asyncio.fixture
async def token(client, user):
    response = await client.post(
        "/api/v1/auth/token",
        data = {"username": user.email, "password": user.clean_password},
    )
    return response.json()["access_token"]

@pytest_asyncio.fixture
async def refresh_token(client, user):
    response = await client.post(
        "/api/v1/auth/token",
        data = {"username": user.email, "password": user.clean_password},
    )
    return response.json()["refresh_token"]

