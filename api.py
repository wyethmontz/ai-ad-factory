from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from workflows.ad_pipeline import run_pipeline
from core.db import save_ad, supabase
from core.job_store import jobs
from core.analytics import get_summary
from agents.optimizer import run_optimizer

app = FastAPI()

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


def _run_job(job_id: str, input_data: dict):
    """Background task that runs the full ad pipeline."""
    try:
        result = run_pipeline(
            input_data,
            on_step=lambda step: jobs.update_step(job_id, step),
        )
        if isinstance(result, dict) and "error" in result:
            jobs.fail_job(job_id, result["error"])
        else:
            jobs.complete_job(job_id, result)
    except Exception as e:
        jobs.fail_job(job_id, str(e))


@app.post("/generate-ad")
def generate_ad(request: AdRequest, background_tasks: BackgroundTasks):
    input_data = {
        "product": request.product,
        "audience": request.audience,
        "platform": request.platform,
        "goal": request.goal,
    }

    job_id = jobs.create_job(input_data)
    background_tasks.add_task(_run_job, job_id, input_data)

    return {"job_id": job_id, "status": "pending"}


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    job = jobs.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@app.get("/ads")
def list_ads(search: str = ""):
    query = supabase.table("ads").select("*").order("created_at", desc=True)
    if search:
        query = query.ilike("product", f"%{search}%")
    return query.execute().data


@app.get("/ads/{ad_id}")
def get_ad(ad_id: str):
    result = supabase.table("ads").select("*").eq("id", ad_id).single().execute()
    return result.data


@app.get("/analytics/summary")
def analytics_summary():
    return get_summary()


@app.get("/analytics/insights")
def analytics_insights():
    try:
        insights = run_optimizer()
        return {"insights": insights or "Not enough data yet. Generate at least 3 ads."}
    except Exception as e:
        return {"insights": f"Could not generate insights: {str(e)}"}
