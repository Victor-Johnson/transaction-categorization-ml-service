import json
from pathlib import Path
from datetime import datetime
import joblib

MODEL_IN = Path("models/model.joblib")
META_IN = Path("models/metadata.json")

OUT_DIR = Path("artifacts") / datetime.utcnow().strftime("%Y%m%d_%H%M%S")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    if not MODEL_IN.exists():
        raise FileNotFoundError("models/model.joblib not found.")
    if not META_IN.exists():
        raise FileNotFoundError("models/metadata.json not found.")

    # copying  model
    model = joblib.load(MODEL_IN)
    joblib.dump(model, OUT_DIR / "model.joblib")

    meta = json.loads(META_IN.read_text())
    meta["frozen_at_utc"] = datetime.utcnow().isoformat() + "Z"
    meta["artifact_dir"] = str(OUT_DIR)

    (OUT_DIR / "metadata.json").write_text(json.dumps(meta, indent=2))
    (Path("artifacts") / "LATEST").write_text(str(OUT_DIR))

    print(f" frozen model to: {OUT_DIR}")
    print(f" updated artifacts/LATEST -> {OUT_DIR}")

if __name__ == "__main__":
    main()