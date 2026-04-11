from core.llm import call_claude

def run_copywriter(input_data):
    hook = input_data["hook"]
    angle = input_data["angle"]

    prompt = f"""You are a senior ad copywriter at a top cosmetics brand.

Write a complete, high-converting ad script for social media.

HOOK: {hook}
ANGLE: {angle}

Requirements:
- Open with an attention-grabbing first line using the hook
- Build desire using the angle throughout
- Include specific, vivid language (not generic marketing speak)
- End with a clear, urgent call-to-action
- Keep it 100-150 words (perfect for TikTok/Reels)
- Write in a conversational, relatable tone

Return in this format:

SCRIPT:
[the full ad script]

CTA:
[the call-to-action line]
"""

    return call_claude(prompt)
