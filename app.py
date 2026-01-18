from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import pickle
import io

from pred import pred

app = FastAPI()
templates = Jinja2Templates(directory="templates")

with open("catboost_model.pkl", "rb") as f:
    model = pickle.load(f)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    df = pred(pd.read_csv(io.BytesIO(contents)))

    preds = model.predict(df)
    probs = model.predict_proba(df)[:, 1]  # вероятность высокого риска

    result = pd.DataFrame({
        "id": df.index,
        "prediction": preds,
        "probability": probs.round(3),
        "risk": ["Высокий" if p == 1 else "Низкий" for p in preds]
    })

    return result.to_dict(orient="records")
