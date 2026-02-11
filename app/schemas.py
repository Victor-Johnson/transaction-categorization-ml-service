from pydantic import BaseModel, Field
from typing import Optional, List

class PredictRequest(BaseModel):
    description: str = Field(..., min_length=1)
    amount: Optional[float] = None
    date: Optional[str] = None

class PredictResponse(BaseModel):
    category: str
    confidence: float
    model_version: str

class BatchPredictRequest(BaseModel):
    items: List[PredictRequest] = Field(..., min_items=1, max_items=500)

class BatchPredictResponse(BaseModel):
    results: List[PredictResponse]
    model_version: str
    