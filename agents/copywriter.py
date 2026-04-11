from core.llm import call_claude

def run_copywriter(input_data):
    hook = input_data["hook"]
    angle = input_data["angle"]

    prompt = f"""
You are a senior ad copywriter.

Create a high-converting ad script.

Hook: {hook}
Angle: {angle}

Return:
Script:
CTA:
"""

    return call_claude(prompt)