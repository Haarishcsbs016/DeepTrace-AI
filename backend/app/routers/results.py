from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.auth.deps import get_current_user
from app.models.user import User
from app.db.mongodb import get_db
import io
import json

router = APIRouter()


@router.get("/history")
async def history(user: User = Depends(get_current_user), limit: int = 50):
    db = get_db()
    if not db:
        return {"items": []}
    cursor = db.results.find({"user_id": user.id}).sort("_id", -1).limit(limit)
    items = await cursor.to_list(length=limit)
    for item in items:
        item["id"] = str(item.pop("_id"))
    return {"items": items}


@router.get("/report/{report_id}")
async def get_report(report_id: str, user: User = Depends(get_current_user)):
    db = get_db()
    if not db:
        raise HTTPException(404, "Report not found")
    doc = await db.results.find_one({"report_id": report_id, "user_id": user.id})
    if not doc:
        raise HTTPException(404, "Report not found")
    doc["id"] = str(doc.pop("_id"))
    return doc


@router.get("/report/{report_id}/download")
async def download_report(report_id: str, user: User = Depends(get_current_user)):
    db = get_db()
    if not db:
        raise HTTPException(404, "Report not found")
    doc = await db.results.find_one({"report_id": report_id, "user_id": user.id})
    if not doc:
        raise HTTPException(404, "Report not found")
    doc["id"] = str(doc.get("_id", ""))
    if "_id" in doc:
        del doc["_id"]
    content = json.dumps(doc, indent=2)
    return StreamingResponse(
        io.BytesIO(content.encode()),
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename=deepfake_report_{report_id}.json"},
    )
