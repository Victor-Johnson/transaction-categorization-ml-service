from pathlib import Path
import joblib
import numpy as np
import json

LATEST_PTR = Path("artifacts") / "LATEST"

class ModelService:
    def __init__(self):
        if not LATEST_PTR.exists():
            raise FileNotFoundError("artifacts/LATEST not found. Run: python training/freeze_model.py")

        self.artifact_dir = Path(LATEST_PTR.read_text().strip())
        self.model = joblib.load(self.artifact_dir / "model.joblib")

        meta_path = self.artifact_dir / "metadata.json"
        self.meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
        self.version = self.artifact_dir.name

    def predict_one(self, description: str):
        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba([description])[0]
            idx = int(np.argmax(probs))
            pred = str(self.model.classes_[idx])
            conf = float(probs[idx])
            return pred, conf
        pred = str(self.model.predict([description])[0])
        return pred, 1.0

    def predict_many(self, descriptions):
        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(descriptions)
            idxs = probs.argmax(axis=1)
            preds = [str(self.model.classes_[i]) for i in idxs]
            confs = [float(probs[r, i]) for r, i in enumerate(idxs)]
            return preds, confs
        preds = [str(x) for x in self.model.predict(descriptions)]
        return preds, [1.0] * len(preds)