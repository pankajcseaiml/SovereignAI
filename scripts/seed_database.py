"""
SovereignAI — Database Seeder
Seeds initial superuser, engineer user, sample industrial conversation, messages, and document records.
"""

import sys
import asyncio
from pathlib import Path

# Add backend to pythonpath
backend_path = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.core.database import AsyncSessionLocal, engine, Base
from app.models.user import User
from app.models.conversation import Conversation, Message
from app.models.document import Document
from sqlalchemy.future import select


async def seed():
    print("[*] Connecting to database and creating tables if not present...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        # Check if users already exist
        res = await session.execute(select(User).where(User.username == "admin"))
        existing_admin = res.scalars().first()

        if not existing_admin:
            print("[*] Seeding default users...")
            admin_user = User(
                id=1,
                username="admin",
                email="admin@sovereign.local",
                hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
                is_active=True,
                is_superuser=True
            )
            eng_user = User(
                id=2,
                username="engineer_pankaj",
                email="engineer@sovereign.local",
                hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
                is_active=True,
                is_superuser=False
            )
            session.add_all([admin_user, eng_user])
            await session.commit()
            print("  [+] Created users: 'admin' and 'engineer_pankaj'")
        else:
            print("[*] Admin user already exists. Skipping user seed.")

        # Seed conversation
        res_conv = await session.execute(select(Conversation).where(Conversation.id == "conv_turbopump_audit"))
        existing_conv = res_conv.scalars().first()
        if not existing_conv:
            print("[*] Seeding sample industrial conversation & messages...")
            conv = Conversation(
                id="conv_turbopump_audit",
                title="Turbopump Valve Inspection & Safety Audit",
                user_id=2
            )
            msg1 = Message(
                id="msg_001",
                conversation_id="conv_turbopump_audit",
                role="user",
                content="Please review the inspection log for Valve B-12 and verify standard operating pressure.",
                metadata_json={"source": "web_chat"}
            )
            msg2 = Message(
                id="msg_002",
                conversation_id="conv_turbopump_audit",
                role="assistant",
                content="According to Standard Operating Procedure SOP-774, Valve B-12 nominal operating pressure is 450 PSI (+/- 15 PSI). The latest inspection reading showed 448 PSI, which is well within normal safe operating thresholds.",
                metadata_json={"agent": "industrial_sop_agent", "confidence": 0.98}
            )
            session.add_all([conv, msg1, msg2])
            await session.commit()
            print("  [+] Created demo conversation 'conv_turbopump_audit'")
        else:
            print("[*] Demo conversation already exists.")

        # Seed document
        res_doc = await session.execute(select(Document).where(Document.id == 1))
        existing_doc = res_doc.scalars().first()
        if not existing_doc:
            print("[*] Seeding sample document...")
            doc = Document(
                id=1,
                filename="Turbopump_Inspection_Report_2026.pdf",
                filepath="/storage/uploads/dummy.pdf",
                mime_type="application/pdf",
                status="completed",
                user_id=2
            )
            session.add(doc)
            await session.commit()
            print("  [+] Created demo document record.")
        else:
            print("[*] Demo document already exists.")

    print("[SUCCESS] Database seeding complete!")


def main():
    try:
        asyncio.run(seed())
    except Exception as e:
        print(f"[ERROR] Database seeding failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
