from fastapi import FastAPI
from app.schemas import PredictRequest, PredictResponse, BatchPredictRequest, BatchPredictResponse
from app.model import ModelService
import time

app = FastAPI(title="Transaction Categorization Service", version="0.1.0")
svc = ModelService()

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_version": svc.version,
        "labels": svc.meta.get("labels", []),
    }

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    t0 = time.time()
    cat, conf = svc.predict_one(req.description)
    _ms = int((time.time() - t0) * 1000)
    return PredictResponse(category=cat, confidence=conf, model_version=svc.version)

@app.post("/predict/batch", response_model=BatchPredictResponse)
def predict_batch(req: BatchPredictRequest):
    t0 = time.time()
    descriptions = [x.description for x in req.items]
    preds, confs = svc.predict_many(descriptions)
    _ms = int((time.time() - t0) * 1000)

    results = [
        PredictResponse(category=p, confidence=c, model_version=svc.version)
        for p, c in zip(preds, confs)
    ]
    return BatchPredictResponse(results=results, model_version=svc.version)