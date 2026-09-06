import sys
import pytest
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.future import select

backend_dir = Path(__file__).resolve().parent.parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.core.database import Base
from app.models.user import User
from app.models.conversation import Conversation, Message
from app.models.document import Document


@pytest.fixture
async def async_db():
    """Provides an isolated in-memory SQLite database for model verification."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as session:
        yield session

    await engine.dispose()


@pytest.mark.asyncio
async def test_user_creation(async_db: AsyncSession):
    """Verify User model creation and querying."""
    user = User(
        username="test_operator",
        email="operator@sovereign.local",
        hashed_password="test_hashed_secret",
        is_active=True,
        is_superuser=False
    )
    async_db.add(user)
    await async_db.commit()

    result = await async_db.execute(select(User).where(User.username == "test_operator"))
    found = result.scalars().first()
    assert found is not None
    assert found.email == "operator@sovereign.local"
    assert found.is_active is True


@pytest.mark.asyncio
async def test_conversation_and_message_relationship(async_db: AsyncSession):
    """Verify Conversation and Message models with cascade relationships."""
    conv = Conversation(id="conv_test_101", title="Inspection Chat")
    async_db.add(conv)
    await async_db.commit()

    msg = Message(
        id="msg_test_001",
        conversation_id="conv_test_101",
        role="user",
        content="Check pump pressure."
    )
    async_db.add(msg)
    await async_db.commit()

    result = await async_db.execute(select(Conversation).where(Conversation.id == "conv_test_101"))
    found_conv = result.scalars().first()
    assert found_conv is not None
    assert found_conv.title == "Inspection Chat"


@pytest.mark.asyncio
async def test_document_creation(async_db: AsyncSession):
    """Verify Document model creation and status progression."""
    doc = Document(
        filename="safety_protocol.pdf",
        filepath="/storage/uploads/safety_protocol.pdf",
        mime_type="application/pdf",
        status="pending"
    )
    async_db.add(doc)
    await async_db.commit()

    result = await async_db.execute(select(Document).where(Document.filename == "safety_protocol.pdf"))
    found_doc = result.scalars().first()
    assert found_doc is not None
    assert found_doc.status == "pending"
