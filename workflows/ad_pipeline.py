import json
from agents.strategist import run_strategist
from agents.copywriter import run_copywriter
from agents.creative import run_creative
from agents.qa import run_qa
from agents.media import run_media
from core.db import save_ad

def run_pipeline(input_data):

    # STEP 1 — STRATEGIST (RAW AI TEXT)
    strategy_raw = run_strategist(input_data)

    print("\n[RAW STRATEGIST OUTPUT]\n")
    print(strategy_raw)

    # STEP 2 — CONVERT TEXT → JSON
    try:
        strategy = json.loads(strategy_raw)
    except:
        print("\nERROR: AI did not return valid JSON")
        return strategy_raw

    # STEP 3 — COPYWRITER
    copy = run_copywriter(strategy)

    # STEP 4 — CREATIVE DIRECTOR
    creative = run_creative({
        "script": copy
    })

    # STEP 5 — QA CHECK
    qa = run_qa({
        "content": creative
    })

    # STEP 6 — MEDIA GENERATION
    media = run_media({
        "scenes": creative
    })

    # ---------------------------
    # STEP 7 — SAVE TO SUPABASE (PHASE 6)
    # ---------------------------
    final_payload = {
        "product": input_data["product"],
        "hook": strategy.get("hook", ""),
        "angle": strategy.get("angle", ""),
        "positioning": strategy.get("positioning", ""),
        "copy": copy,
        "creative": creative,
        "qa_score": qa,
        "media": media
    }

    # This pushes the data to the cloud!
    save_ad(final_payload)

    return final_payload
