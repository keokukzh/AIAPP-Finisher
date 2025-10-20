"""
Model Routes for KI-Projektmanagement-System
Handles LLM model management and configuration
"""

import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/models", tags=["models"])


class ModelSelectionRequest(BaseModel):
    """Request model for selecting an LLM model"""

    model_name: str
    model_type: str


@router.get("")
async def list_models(model_manager):
    """Lists all available LLM models"""
    try:
        models = await model_manager.list_available_models()

        return {"status": "success", "models": models}

    except Exception as e:
        logger.error(f"❌ Error listing models: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/set")
async def set_model(request: ModelSelectionRequest, model_manager):
    """Sets the active LLM model"""
    try:
        success = await model_manager.set_model(request.model_name, request.model_type)

        if not success:
            raise HTTPException(status_code=400, detail="Failed to set model")

        return {"status": "success", "model": request.model_name, "type": request.model_type}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error setting model: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/current")
async def get_current_model(model_manager):
    """Returns the currently active model"""
    try:
        current = model_manager.current_model

        if not current:
            return {"status": "no_model_selected", "model": None}

        return {"status": "success", "model": current}

    except Exception as e:
        logger.error(f"❌ Error getting current model: {e}")
        raise HTTPException(status_code=500, detail=str(e))
