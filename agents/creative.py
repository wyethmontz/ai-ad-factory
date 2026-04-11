from core.llm import call_claude

def run_creative(input_data):
    script = input_data["script"]

    prompt = f"""
You are a creative director.

Break this script into scenes and visual plan.

Script:
{script}

Return:
Scenes:
Visual Plan:
"""

    return call_claude(prompt)