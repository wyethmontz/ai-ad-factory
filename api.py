from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from workflows.ad_pipeline import run_pipeline
from core.db import save_ad, supabase

app = FastAPI()

# ✅ MUST BE HERE (BEFORE ROUTES)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AdRequest(BaseModel):
    product: str
    audience: str
    platform: str
    goal: str


@app.post("/generate-ad")
def generate_ad(request: AdRequest):

    input_data = {
        "product": request.product,
        "audience": request.audience,
        "platform": request.platform,
        "goal": request.goal
    }

    return run_pipeline(input_data)