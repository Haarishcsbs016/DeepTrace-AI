from fastapi import APIRouter, Depends
from app.auth.deps import get_current_user, require_admin
from app.models.user import User
from app.db.mongodb import get_db

router = APIRouter()


@router.get("/analytics")
async def analytics(user: User = Depends(require_admin)):
    db = get_db()
    if not db:
        return {"total_detections": 0, "by_type": {}, "recent_activity": []}
    total = await db.results.count_documents({})
    pipeline = [{"$group": {"_id": "$media_type", "count": {"$sum": 1}}}]
    by_type = {}
    async for doc in db.results.aggregate(pipeline):
        by_type[doc["_id"]] = doc["count"]
    recent = await db.results.find().sort("_id", -1).limit(20).to_list(20)
    return {
        "total_detections": total,
        "by_type": by_type,
        "recent_activity": [{"report_id": r["report_id"], "label": r["label"], "media_type": r["media_type"]} for r in recent],
    }


@router.get("/users")
async def list_users(user: User = Depends(require_admin)):
    # Placeholder: would query PostgreSQL users with pagination
    return {"users": [], "message": "Implement user list from PostgreSQL"}
