from core.llm import call_claude

def run_media(input_data):

    scenes = input_data["scenes"]

    # 🧪 EXAMPLE SCENES:
    # 1. Girl applies lip tint incorrectly
    # 2. Close-up showing mistake
    # 3. Fix demonstration

    prompt = f"""
You are a visual prompt engineer.

Convert scenes into AI image prompts.

EXAMPLE:
Scene: Girl applying lip tint incorrectly
Output: "young woman applying lip tint incorrectly, soft lighting, beauty aesthetic, TikTok style"

REAL SCENES:
{scenes}

Return ONLY image prompts.
"""

    return call_claude(prompt)