import json
import re
from agents.strategist import run_strategist
from agents.copywriter import run_copywriter
from agents.creative import run_creative
from agents.qa import run_qa
from agents.media import run_media
from agents.optimizer import run_optimizer
from core.db import save_ad

def run_pipeline(input_data, on_step=None):

    def _step(name):
        print(f"\n[STEP: {name}]")
        if on_step:
            on_step(name)

    # STEP 0 — OPTIMIZER (learn from past ads)
    _step("Analyzing past ad performance...")
    try:
        insights = run_optimizer()
    except Exception:
        insights = None  # Don't block pipeline if optimizer fails

    # STEP 1 — STRATEGIST (RAW AI TEXT)
    _step("Running strategist...")
    strategy_raw = run_strategist(input_data, insights=insights)

    print("\n[RAW STRATEGIST OUTPUT]\n")
    print(strategy_raw)

    # STEP 2 — CONVERT TEXT → JSON
    # Strip markdown code fences (```json ... ``` or ``` ... ```) if present
    cleaned = re.sub(r"```(?:json)?\s*", "", strategy_raw).strip()
    # Extract the first {...} block in case Claude added surrounding text
    json_match = re.search(r'\{.*\}', cleaned, re.DOTALL)
    try:
        strategy = json.loads(json_match.group() if json_match else cleaned)
    except (json.JSONDecodeError, AttributeError):
        print("\nERROR: AI did not return valid JSON")
        print("Cleaned output was:", cleaned)
        return {"error": "AI did not return valid JSON", "raw": strategy_raw}

    # STEP 3 — COPYWRITER
    _step("Writing ad copy...")
    copy = run_copywriter(strategy)

    # STEP 4 — CREATIVE DIRECTOR
    _step("Creating visual scenes...")
    creative = run_creative({
        "script": copy
    })

    # STEP 5 — QA CHECK
    _step("Running QA evaluation...")
    qa = run_qa({
        "content": creative
    })

    # STEP 6 — MEDIA GENERATION
    _step("Generating media prompts...")
    media = run_media({
        "scenes": creative
    })

    # ---------------------------
    # STEP 7 — SAVE TO SUPABASE (PHASE 6)
    # ---------------------------

    # Extract numeric QA score for analytics
    score_match = re.search(r'\d+', qa or "")
    qa_numeric = int(score_match.group()) if score_match else None

    final_payload = {
        "product": input_data["product"],
        "audience": input_data.get("audience", ""),
        "platform": input_data.get("platform", ""),
        "goal": input_data.get("goal", ""),
        "hook": strategy.get("hook", ""),
        "angle": strategy.get("angle", ""),
        "positioning": strategy.get("positioning", ""),
        "copy": copy,
        "creative": creative,
        "qa_score": qa,
        "qa_score_numeric": qa_numeric,
        "media": media
    }

    # This pushes the data to the cloud!
    save_ad(final_payload)

    return final_payload
