from core.llm import call_claude

def run_creative(input_data):
    script = input_data["script"]

    prompt = f"""You are a creative director at a social media ad agency.

Break this ad script into a detailed visual production plan.

SCRIPT:
{script}

Return in this format:

SCENES:
Scene 1: [what the viewer sees, camera angle, action]
Scene 2: [...]
Scene 3: [...]
(add more scenes as needed)

VISUAL STYLE:
[overall aesthetic, color palette, lighting, mood]

SHOT LIST:
[specific camera movements, transitions, timing notes]
"""

    return call_claude(prompt)
