import os
import aiofiles
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.document import Document
from app.worker import process_document_task

router = APIRouter()

UPLOAD_DIR = "/app/storage"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
        
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # Save file asynchronously
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
        
    # Create DB record
    new_doc = Document(filename=file.filename, filepath=file_path, status="pending_processing")
    db.add(new_doc)
    await db.commit()
    await db.refresh(new_doc)
    
    # Trigger Celery processing task
    process_document_task.delay(new_doc.id, file_path)
    
    return {
        "id": new_doc.id,
        "filename": new_doc.filename,
        "status": new_doc.status
    }

@router.get("/")
async def list_documents(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Document))
    documents = result.scalars().all()
    return [{"id": d.id, "filename": d.filename, "status": d.status} for d in documents]
