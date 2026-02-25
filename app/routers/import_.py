from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.services.import_scanner import scan_directory
from app.core.config import settings

router = APIRouter(prefix="/api/v1/import", tags=["import"])


class ScanRequest(BaseModel):
    path: Optional[str] = None


class ScanResponse(BaseModel):
    scanned: int
    imported: int
    skipped: int
    errors: List[str]


@router.post("/scan", response_model=ScanResponse)
async def scan_legacy_models(request: ScanRequest):
    path = request.path or settings.legacy_models_path

    try:
        results = await scan_directory(path)
        return ScanResponse(**results)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error scanning directory: {str(e)}",
        )
