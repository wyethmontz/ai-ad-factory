from core.llm import call_claude

def run_media(input_data):
    scenes = input_data["scenes"]

    prompt = f"""You are a visual prompt engineer specializing in AI image generation.

Convert these ad scenes into detailed prompts for AI image tools (Midjourney, DALL-E, Flux).

SCENES:
{scenes}

For each scene, create a prompt that includes:
- Subject and action
- Lighting and mood
- Camera angle and framing
- Style reference (e.g., "TikTok aesthetic", "beauty editorial")
- Color palette

Return each prompt on its own line, numbered:

1. [detailed image prompt for scene 1]
2. [detailed image prompt for scene 2]
3. [...]
"""

    return call_claude(prompt)
